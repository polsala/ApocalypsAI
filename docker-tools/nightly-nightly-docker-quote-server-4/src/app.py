from flask import Flask, jsonify, request
import random

app = Flask(__name__)

QUOTES = [
    "When the sky falls, remember to bring an umbrella.",
    "Even the strongest bunker needs a good Wi‑Fi signal.",
    "Radiation is just nature's way of saying 'you need a break'.",
    "Survive the apocalypse by mastering the art of coffee brewing.",
    "If the world ends, at least you have a playlist."
]

@app.route("/quote")
def quote():
    idx = request.args.get("index")
    if idx is not None and idx.isdigit():
        i = int(idx) % len(QUOTES)
        selected = QUOTES[i]
    else:
        selected = random.choice(QUOTES)
    return jsonify({"quote": selected})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
