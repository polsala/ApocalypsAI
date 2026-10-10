from flask import Flask, request, jsonify
import time

app = Flask(__name__)

QUOTES = [
    "Keep calm and 🍵 on.",
    "May the 🦄 be with you.",
    "Stay pawsitive! 🐾",
    "When life gives you lemons, make 🍋ade.",
    "Adventure awaits! 🌟"
]

def select_quote(seed: int) -> str:
    """Return a quote deterministically based on the integer seed."""
    return QUOTES[seed % len(QUOTES)]

@app.route("/quote")
def quote():
    seed_param = request.args.get("seed")
    if seed_param and seed_param.isdigit():
        seed = int(seed_param)
    else:
        seed = int(time.time())
    return jsonify({"quote": select_quote(seed)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
