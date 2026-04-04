import random
from flask import Flask, jsonify

app = Flask(__name__)

QUOTES = [
    {"quote": "The only limit to our realization of tomorrow is our doubts of today.", "author": "Franklin D. Roosevelt"},
    {"quote": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein"},
    {"quote": "Life is what happens when you're busy making other plans.", "author": "John Lennon"},
]

@app.route("/quote")
def quote():
    return jsonify(random.choice(QUOTES))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
