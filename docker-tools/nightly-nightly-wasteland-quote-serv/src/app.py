import random
from flask import Flask, jsonify

app = Flask(__name__)

QUOTES = [
    "The sun rises, but the world is still ash.",
    "Hope is a scarce resource; ration it wisely.",
    "Even in ruins, a seed can find a crack.",
    "Silence is louder than the last siren.",
    "When the wind howls, listen for opportunity."
]

@app.route("/quote")
def quote():
    return jsonify({"quote": random.choice(QUOTES)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
