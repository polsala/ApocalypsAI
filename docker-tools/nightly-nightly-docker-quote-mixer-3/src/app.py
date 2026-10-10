import random
from flask import Flask, jsonify

app = Flask(__name__)

QUOTES = [
    "The sun rises, but the shadows linger.",
    "Hope is a candle in the wasteland.",
    "When the world ends, coffee still brews.",
    "Survival is a joke told by the wind.",
    "Dreams are the last radio signals."
]

@app.route("/quote")
def quote():
    # deterministic for testing if seed set
    selected = random.choice(QUOTES)
    return jsonify({"quote": selected})

if __name__ == "__main__":
    # Use port 8080
    app.run(host="0.0.0.0", port=8080)
