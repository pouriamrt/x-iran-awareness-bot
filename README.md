# X Iran Awareness Bot

An automated X (Twitter) bot that uses LLM to generate and post Iran awareness content on a scheduled basis with OAuth2 authentication.

## Features

- 🤖 **LLM-Powered Content Generation**: Uses OpenAI's GPT models to generate impactful posts about Iran awareness
- 🔐 **OAuth2 PKCE Authentication**: Secure authentication flow with automatic token management
- 🔄 **Automatic Token Refresh**: Handles token expiration and refresh automatically
- ⏰ **Scheduled Posting**: Posts content every 30 minutes automatically
- 🛡️ **Error Handling**: Robust error handling with automatic retry and re-authentication
- 🌐 **Browser-Based Auth**: Seamless OAuth flow with automatic browser opening

## Prerequisites

- Python 3.13 or higher
- X (Twitter) Developer Account with API access
- OpenAI API key
- `uv` package manager (recommended) or `pip`

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd X_bot
   ```

2. **Install dependencies using `uv` (recommended):**
   ```bash
   uv sync
   ```

   Or using `pip`:
   ```bash
   pip install -e .
   ```

## Configuration

1. **Create a `.env` file in the project root:**
   ```env
   # X (Twitter) API Credentials
   X_CLIENT_ID=your_client_id_here
   X_CLIENT_SECRET=your_client_secret_here
   X_REDIRECT_URI=http://127.0.0.1:8080/callback

   # OpenAI API Key
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **Get X API Credentials:**
   - Go to [X Developer Portal](https://developer.twitter.com/)
   - Create a new app or use an existing one
   - Generate OAuth 2.0 credentials (Client ID and Client Secret)
   - Set the redirect URI to match `X_REDIRECT_URI` in your `.env` file

3. **Get OpenAI API Key:**
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Generate an API key from your account settings

## Usage

1. **Run the bot:**
   ```bash
   uv run python main.py
   ```

   Or with `pip`:
   ```bash
   python main.py
   ```

2. **First-time Authorization:**
   - The bot will automatically open your browser for X authorization
   - Complete the OAuth flow in the browser
   - The authorization tokens will be saved to `tokens.json`
   - You can close the browser tab after authorization

3. **Automatic Operation:**
   - The bot will generate a post using the LLM
   - Post it to X/Twitter
   - Wait 30 minutes before posting again
   - This cycle continues indefinitely

## How It Works

1. **Authentication Flow:**
   - On first run, the bot opens a browser for OAuth2 PKCE authentication
   - A local HTTP server listens for the OAuth callback
   - Tokens are saved to `tokens.json` for future use

2. **Content Generation:**
   - The bot uses OpenAI's GPT model to generate posts about Iran awareness
   - Posts include relevant hashtags and mentions of world leaders
   - Content is generated to stay within X's 280-character limit

3. **Posting Cycle:**
   - Generates a new post every 30 minutes
   - Automatically handles token refresh if needed
   - Retries with token refresh on failure
   - Falls back to re-authentication if refresh fails

4. **Error Recovery:**
   - If posting fails, the bot attempts to refresh the access token
   - If refresh fails, it removes old tokens and re-authenticates
   - The bot continues running even after errors

## Project Structure

```
X_bot/
├── main.py           # Main bot logic and OAuth flow
├── llm.py            # LLM content generation
├── pyproject.toml    # Project dependencies and metadata
├── tokens.json       # Saved OAuth tokens (generated at runtime)
├── .env              # Environment variables (create this)
└── README.md         # This file
```

## Troubleshooting

### Bot gets stuck when opening browser
- The bot now includes a 5-minute timeout for OAuth callbacks
- If authorization takes too long, the bot will show an error message
- Simply restart the bot and complete the authorization quickly

### Token expiration errors
- The bot automatically handles token refresh
- If refresh fails, it will re-authenticate automatically
- Old tokens are cleared and a new OAuth flow is initiated

### LLM generation fails
- The bot includes a fallback message if LLM generation fails
- Check your OpenAI API key and account balance
- Ensure you have internet connectivity

### Port already in use
- Change the `X_REDIRECT_URI` in your `.env` to use a different port
- Update the redirect URI in your X Developer Portal app settings

## License

See the [LICENSE](LICENSE) file for details.

## Disclaimer

This bot is designed for awareness purposes. Ensure you comply with X/Twitter's Terms of Service and API usage policies. Use responsibly and respect rate limits.
