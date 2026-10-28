# Terminal Chatbot

A simple chatbot you run in the terminal, powered by the Anthropic API. It remembers the conversation during a session. It uses only the Python standard library, so there's nothing to install with pip.

## Requirements

- Python 3.8 or newer
- An Anthropic API key from https://console.anthropic.com (API usage is billed per use)

## Setup

Set your API key in the terminal session before running the app. Don't put the key inside the code.

Windows (PowerShell):

```powershell
$env:ANTHROPIC_API_KEY="your-key-here"
```

Mac or Linux:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

## Run

```bash
python chatbot.py
```

Commands inside the chat:

- `/clear` starts a new conversation
- `/exit` quits

## Customizing

Open `chatbot.py` and edit the settings at the top:

- `SYSTEM_PROMPT` sets the bot's role, for example "You are a tutor for Indian polity questions."
- `MAX_HISTORY_MESSAGES` controls how much past conversation is kept, which affects cost.
- `MAX_REPLY_TOKENS` limits the length of each reply.

To use a different model, set the `CHAT_MODEL` environment variable, or change `MODEL` in the file.

## Project files

- `chatbot.py`: the chatbot program
- `README.md`: these instructions

## Publishing to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

Never commit your API key. Because the key is read from an environment variable, it stays out of the code. As an extra safeguard, you can add a `.gitignore` file with a `.env` line if you ever store the key in a file.
