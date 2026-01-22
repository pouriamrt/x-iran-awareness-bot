import base64
import json
import os
import sys
import time
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.parse import urlparse

from dotenv import load_dotenv
from xdk import Client
from xdk.oauth2_auth import OAuth2PKCEAuth

from llm import generate_iran_post

load_dotenv()

TOKENS_FILE = "tokens.json"
client_id = os.environ.get("X_CLIENT_ID")
client_secret = os.environ.get("X_CLIENT_SECRET")
redirect_uri = os.environ.get("X_REDIRECT_URI")
scopes = ["tweet.read", "tweet.write", "users.read", "offline.access"]


def _parse_redirect_uri(uri: str) -> tuple[str, int, str]:
    parsed = urlparse(uri)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    path = parsed.path or "/"
    return host, port, path


def _run_callback_server(host: str, port: int, base_path: str, redirect_base: str) -> str:
    callback_url_container: list[str] = []
    timeout_seconds = 300  # 5 minutes timeout

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith(base_path) or (base_path == "/" and self.path.startswith("/")):
                # Reconstruct full callback URL (redirect_uri + query)
                if "?" in self.path:
                    path, qs = self.path.split("?", 1)
                    full = f"{redirect_base}?{qs}"
                else:
                    full = redirect_base
                callback_url_container.append(full)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            body = (
                b"<html><body><h1>Authorization successful</h1>"
                b"<p>You can close this tab and return to the app.</p></body></html>"
            )
            self.wfile.write(body)

        def log_message(self, format, *args):
            pass

    server = HTTPServer((host, port), CallbackHandler)
    server.timeout = 1  # Set socket timeout to 1 second
    
    def handle_request_with_timeout():
        import time as time_module
        start_time = time_module.time()
        while time_module.time() - start_time < timeout_seconds:
            try:
                server.handle_request()
                # If we get here, a request was handled (or timeout occurred)
                if callback_url_container:
                    break
            except Exception:
                # Timeout or other error, continue waiting
                pass
    
    thread = Thread(target=handle_request_with_timeout, daemon=True)
    thread.start()
    thread.join(timeout=timeout_seconds)
    
    # Ensure server is closed
    try:
        server.server_close()
    except Exception:
        pass
    
    if thread.is_alive():
        raise RuntimeError(
            f"OAuth callback timeout after {timeout_seconds} seconds. "
            "Please complete the authorization in the browser and try again."
        )
    
    if not callback_url_container:
        raise RuntimeError("Callback server did not receive the redirect URL.")
    return callback_url_container[0]


def load_tokens() -> dict | None:
    if not os.path.exists(TOKENS_FILE):
        return None
    with open(TOKENS_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_tokens(tokens: dict) -> None:
    with open(TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=2)


def refresh_access_token() -> str:
    data = load_tokens()
    if not data or "refresh_token" not in data:
        raise RuntimeError("No refresh token available. Re-authorize the app.")
    refresh_token = data["refresh_token"]

    url = "https://api.x.com/2/oauth2/token"
    body = f"grant_type=refresh_token&refresh_token={refresh_token}"
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    req = urllib.request.Request(url, data=body.encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        out = json.loads(resp.read().decode())
    access_token = out["access_token"]
    new_tokens = {**data, "access_token": access_token, "token_type": out.get("token_type", "bearer")}
    if "expires_in" in out:
        new_tokens["expires_in"] = out["expires_in"]
    if "refresh_token" in out:
        new_tokens["refresh_token"] = out["refresh_token"]
    save_tokens(new_tokens)
    return access_token


def _run_oauth_flow() -> Client:
    auth = OAuth2PKCEAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scopes,
    )
    auth_url = auth.get_authorization_url()
    host, port, path = _parse_redirect_uri(redirect_uri)
    parsed = urlparse(redirect_uri)
    redirect_base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    print("Opening browser for X authorization…")
    webbrowser.open(auth_url)
    callback_url = _run_callback_server(host, port, path, redirect_base)
    tokens = auth.fetch_token(authorization_response=callback_url)
    save_tokens(dict(tokens))
    return Client(access_token=tokens["access_token"])


def get_valid_client() -> Client:
    tokens = load_tokens()
    if tokens and tokens.get("access_token"):
        return Client(access_token=tokens["access_token"])
    return _run_oauth_flow()


def main() -> None:
    if not all([client_id, client_secret, redirect_uri]):
        print("Missing X_CLIENT_ID, X_CLIENT_SECRET, or X_REDIRECT_URI in environment.", file=sys.stderr)
        sys.exit(1)

    client = get_valid_client()
    interval_seconds = 30 * 60  # 30 minutes

    while True:
        try:
            # Generate a new post using LLM
            print("Generating post using LLM...")
            post_text = generate_iran_post()
            print(f"Generated post: {post_text}")
            payload = {"text": post_text}
            
            response = client.posts.create(body=payload)
            print("Tweet posted successfully.")
            print(json.dumps(response.data, indent=2, sort_keys=True))
        except Exception as e:
            print(f"Post failed: {e}", file=sys.stderr)
            retried = False
            try:
                access_token = refresh_access_token()
                client = Client(access_token=access_token)
                # Regenerate post for retry
                post_text = generate_iran_post()
                payload = {"text": post_text}
                response = client.posts.create(body=payload)
                print("Tweet posted successfully after token refresh.")
                print(json.dumps(response.data, indent=2, sort_keys=True))
                retried = True
            except Exception:
                pass
            if not retried:
                try:
                    if os.path.exists(TOKENS_FILE):
                        os.remove(TOKENS_FILE)
                    client = get_valid_client()
                    # Regenerate post for re-auth retry
                    post_text = generate_iran_post()
                    payload = {"text": post_text}
                    response = client.posts.create(body=payload)
                    print("Tweet posted successfully after re-authorization.")
                    print(json.dumps(response.data, indent=2, sort_keys=True))
                except Exception as auth_err:
                    print(f"Re-auth failed: {auth_err}", file=sys.stderr)
        print(f"Next post in {interval_seconds // 60} minutes…")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    main()
