#!/usr/bin/env python3
"""Terminal chatbot powered by the Anthropic API.

Uses only the Python standard library. Set your API key in the
ANTHROPIC_API_KEY environment variable before running (never in this file).
"""

import json
import os
import sys
import urllib.error
import urllib.request

# ---- Settings you can change -------------------------------------------------

# Give the bot a role. Edit this text to change how it behaves.
SYSTEM_PROMPT = (
    "You are a helpful study assistant. Explain things clearly and simply, "
    "and use short examples where they help."
)

# Model to use. You can override this with the CHAT_MODEL environment variable.
MODEL = os.environ.get("CHAT_MODEL", "claude-haiku-5-5")

# Maximum number of messages kept in memory, to limit cost on long chats.
MAX_HISTORY_MESSAGES = 20

# Maximum length of each reply, in tokens.
MAX_REPLY_TOKENS = 1024

# API address. Normally you don't change this.
API_BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
API_VERSION = "2023-06-01"


# ---- API call ----------------------------------------------------------------

def send_to_claude(api_key, messages):
    """Send the conversation to the API and return the reply text, or None on error."""
    body = {
        "model": MODEL,
        "max_tokens": MAX_REPLY_TOKENS,
        "system": SYSTEM_PROMPT,
        "messages": messages,
    }
    request = urllib.request.Request(
        url=f"{API_BASE_URL}/v1/messages",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": API_VERSION,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        print(f"\n[API error {error.code}] {details}")
        return None
    except urllib.error.URLError as error:
        print(f"\n[Network error] Could not reach the API: {error.reason}")
        return None

    # The reply is a list of content blocks; join the text blocks together.
    parts = [block.get("text", "") for block in data.get("content", []) if block.get("type") == "text"]
    return "".join(parts).strip()


# ---- Chat loop ---------------------------------------------------------------

def trim_history(history):
    """Keep only the most recent messages, and make sure the first one is from the user."""
    if len(history) > MAX_HISTORY_MESSAGES:
        history = history[-MAX_HISTORY_MESSAGES:]
    while history and history[0]["role"] != "user":
        history = history[1:]
    return history


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print("No API key found.")
        print("Set it in your terminal first, then run the chatbot again:")
        print("  Windows (PowerShell):  $env:ANTHROPIC_API_KEY=\"your-key\"")
        print("  Mac/Linux:             export ANTHROPIC_API_KEY=\"your-key\"")
        sys.exit(1)

    print(f"Chatbot ready (model: {MODEL}).")
    print("Type your message and press Enter.")
    print("Commands: /clear to start a new conversation, /exit to quit.\n")

    history = []

    while True:
        try:
            user_text = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_text:
            continue
        if user_text == "/exit":
            print("Goodbye!")
            break
        if user_text == "/clear":
            history = []
            print("Conversation cleared.\n")
            continue

        history.append({"role": "user", "content": user_text})
        history = trim_history(history)

        reply = send_to_claude(api_key, history)
        if reply is None:
            # Remove the unanswered message so the next try starts cleanly.
            history.pop()
            print()
            continue

        history.append({"role": "assistant", "content": reply})
        print(f"\nBot: {reply}\n")


if __name__ == "__main__":
    main()
