import random
from flask import Flask, jsonify

app = Flask(__name__)

QUOTES = [
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "When life gives you lemons, make lemonade... then find someone whose life gave them vodka.",
    "I put the 'pro' in procrastination.",
    "If at first you don't succeed, skydiving is not for you.",
    "Why chase rainbows when you can chase coffee?"
]

def get_random_quote():
    """Return a random quote from the list."""
    return random.choice(QUOTES)

@app.route("/quote")
def quote():
    return jsonify({"quote": get_random_quote()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
