import random
from flask import Flask, jsonify

app = Flask(__name__)

QUOTES = [
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "When life gives you lemons, make lemonade. Then find someone whose life gave them vodka.",
    "In the middle of difficulty lies opportunity… and maybe a snack.",
    "Keep calm and pretend this is a feature, not a bug.",
    "Adventure awaits those who forget to set their GPS."
]

@app.route("/quote")
def quote():
    return jsonify({"quote": random.choice(QUOTES)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
