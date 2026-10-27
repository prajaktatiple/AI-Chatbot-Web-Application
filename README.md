# Nova: AI Chatbot Web Application

A responsive chatbot with a Flask backend and a vanilla JavaScript chat interface.

## Features
- Attractive homepage with starter prompts
- Chat interface with user and bot message bubbles
- Python (Flask) backend at `/api/chat`
- Typing indicator and typewriter-style replies
- Responsive layout (desktop and mobile)
- Chat history sidebar (saved in the browser, deletable)
- Bonus: dark mode, 4 colour themes, voice input (microphone) and read-aloud replies
- Works offline with built-in rules, or with real AI via the OpenAI API

## Run locally
```bash
python -m venv venv
venv\Scripts\activate          # Windows (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Enable real AI answers (optional)
Set an environment variable before running:
```bash
set OPENAI_API_KEY=your-key        # Windows (macOS/Linux: export OPENAI_API_KEY=your-key)
```
Never commit your key. `.env` is git-ignored.

## Deploy on Render (free)
1. Push to GitHub.
2. Render → New Web Service → select the repo.
3. Build: `pip install -r requirements.txt`   Start: `gunicorn app:app`
4. Add `OPENAI_API_KEY` under Environment (optional).

## Tech
Python, Flask, Requests, HTML, CSS, JavaScript, Web Speech API
