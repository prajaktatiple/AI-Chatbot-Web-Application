import os
import re
import random
from datetime import datetime

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
SYSTEM_PROMPT = ("You are Nova, a friendly and concise AI assistant inside a web chat app. "
                 "Answer clearly, use short paragraphs, and ask a follow-up question when helpful.")

# ---------- offline fallback (used when no API key is set) ----------
RULES = [
    (r"\b(hi|hello|hey|namaste)\b", ["Hello! I'm Nova. What would you like to talk about?",
                                      "Hi there! How can I help today?"]),
    (r"\b(your name|who are you)\b", ["I'm Nova, an AI chatbot built with Flask and JavaScript."]),
    (r"\b(how are you)\b", ["Doing great, thanks for asking. How about you?"]),
    (r"\b(help|what can you do)\b", ["I can chat, tell jokes, share the time and date, and do quick maths like 12*7. "
                                      "Connect an OpenAI key to unlock full AI answers."]),
    (r"\b(joke)\b", ["Why do programmers prefer dark mode? Because light attracts bugs.",
                      "A SQL query walks into a bar, sees two tables and asks: can I join you?"]),
    (r"\b(python)\b", ["Python is a readable, general-purpose language, great for web apps (Flask, Django), data science and automation."]),
    (r"\b(flask)\b", ["Flask is a lightweight Python web framework. This chatbot's backend is built with it."]),
    (r"\b(thanks|thank you)\b", ["You're welcome!"]),
    (r"\b(bye|goodbye)\b", ["Goodbye! Come back anytime."]),
]


def local_reply(text: str) -> str:
    t = text.lower().strip()
    if re.search(r"\b(time|date|day)\b", t):
        return "It's " + datetime.now().strftime("%A, %d %B %Y, %I:%M %p") + " on the server."
    m = re.fullmatch(r"[\d\s+\-*/().%]+", t.replace("x", "*"))
    if m and re.search(r"\d", t):
        try:
            return f"{t} = {eval(t.replace('x', '*'), {'__builtins__': {}}, {})}"
        except Exception:
            pass
    for pattern, answers in RULES:
        if re.search(pattern, t):
            return random.choice(answers)
    return ("I'm running in offline mode, so my answers are limited. "
            "Add an OpenAI API key on the server for full AI responses. Meanwhile, try: 'tell me a joke' or '12*7'.")


def ai_reply(history):
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": MODEL, "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + history[-20:]},
        timeout=40,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


@app.route("/")
def index():
    return render_template("index.html", mode="ai" if API_KEY else "offline")


@app.route("/api/chat", methods=["POST"])
def chat():
    body = request.get_json(silent=True) or {}
    history = [m for m in body.get("messages", [])
               if m.get("role") in ("user", "assistant") and str(m.get("content", "")).strip()]
    if not history or history[-1]["role"] != "user":
        return jsonify(error="Type a message first."), 400
    history = [{"role": m["role"], "content": str(m["content"])[:4000]} for m in history]
    if API_KEY:
        try:
            return jsonify(reply=ai_reply(history), mode="ai")
        except Exception:
            return jsonify(reply=local_reply(history[-1]["content"]) + "\n\n(The AI service didn't respond, so this is an offline answer.)", mode="offline")
    return jsonify(reply=local_reply(history[-1]["content"]), mode="offline")


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
