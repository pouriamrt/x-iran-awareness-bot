import os
import sys
from openai import OpenAI
from llms.prompts import SYSTEM_PROMPT, USER_PROMPT
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


MAX_POST_LENGTH = 280
MAX_RETRIES = 3


def _call_llm(messages: list) -> str:
    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL"),
        messages=messages,
        max_completion_tokens=250,
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("LLM returned empty content")
    return content.strip()


def generate_iran_post() -> str:
    """
    Generate a post about the massacre in Iran using LLM.
    Retries up to MAX_RETRIES times if the post exceeds 280 characters.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ]

    try:
        for attempt in range(MAX_RETRIES):
            post_text = _call_llm(messages)
            if len(post_text) <= MAX_POST_LENGTH:
                return post_text
            print(
                f"Post too long ({len(post_text)} chars), retrying ({attempt + 1}/{MAX_RETRIES})...",
                file=sys.stderr,
            )
            messages.append({"role": "assistant", "content": post_text})
            messages.append({
                "role": "user",
                "content": f"That post is {len(post_text)} characters. It MUST be under {MAX_POST_LENGTH} characters. Shorten it while keeping the core message, key hashtags, and a few mentions.",
            })

        # All retries exceeded — truncate as last resort
        print(f"Could not generate post under {MAX_POST_LENGTH} chars after {MAX_RETRIES} retries, truncating.", file=sys.stderr)
        return post_text[:MAX_POST_LENGTH]
    except Exception as e:
        print(f"LLM generation failed: {e}", file=sys.stderr)
        return "The Iranian people are rising for freedom. Support @PahlaviReza and the democratic transition. End the blackout. #JavidShah #IranRevolution #FreeIran @WhiteHouse @antonioguterres"
