from flask import Flask, jsonify
import random

app = Flask(__name__)

QUOTES = [
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "When life gives you lemons, make lemonade... then find someone whose life gave them vodka.",
    "I’m not lazy, I’m on energy‑saving mode.",
    "If at first you don’t succeed, skydiving is not for you.",
    "Why fall in love when you can fall asleep?"
]

@app.route("/", methods=["GET"])
def get_quote():
    return jsonify({"quote": random.choice(QUOTES)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
