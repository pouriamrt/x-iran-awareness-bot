# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

X Iran Awareness Bot — an automated X (Twitter) bot that uses OpenAI's GPT models to generate and post Iran human rights awareness content on a 30-minute interval. Uses OAuth2 PKCE for X API authentication with automatic token refresh.

## Commands

```bash
# Install dependencies
uv sync

# Run the bot
uv run python main.py
```

There are no tests, linter, or build steps configured.

## Architecture

**`main.py`** — Entry point and core bot logic:
- OAuth2 PKCE flow: browser-based auth via local HTTP callback server, token persistence in `tokens.json`
- Token lifecycle: load → check expiry (with 5-min buffer) → refresh via X API → re-auth fallback
- Main loop: generate post → call `client.posts.create()` → sleep 30 min → repeat
- Rate limit handling: parses `x-rate-limit-*` headers, waits until reset time
- Error recovery chain: rate-limit wait → token refresh retry → full re-auth → continue
- Monkey-patches `httpx.Client.request` to log request/response headers (debug aid)

**`llms/`** — LLM content generation module:
- `llm.py`: Calls OpenAI chat completions API using model from `OPENAI_MODEL` env var. Has a hardcoded fallback post if LLM fails.
- `prompts.py`: System and user prompts defining the content generation constraints (280-char limit, hashtags, leader mentions).

## Key Dependencies

- **`xdk`** — X API client library (provides `Client` and `OAuth2PKCEAuth`)
- **`openai`** — OpenAI Python SDK for content generation
- **`python-dotenv`** — Loads `.env` configuration

## Environment Variables (`.env`)

- `X_CLIENT_ID`, `X_CLIENT_SECRET`, `X_REDIRECT_URI` — X OAuth2 credentials
- `OPENAI_API_KEY` — OpenAI API key
- `OPENAI_MODEL` — GPT model name for content generation

## Important Patterns

- The X API client comes from `xdk`, not `tweepy` (tweepy is listed in deps but unused).
- Token refresh uses raw `urllib.request` against `https://api.x.com/2/oauth2/token` with Basic auth, not the xdk client.
- `tokens.json` stores OAuth tokens with an `obtained_at` timestamp for expiry tracking. It is gitignored.
- The bot runs as an infinite loop — there is no graceful shutdown mechanism.
