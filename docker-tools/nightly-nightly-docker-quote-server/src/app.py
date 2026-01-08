from flask import Flask
import random

app = Flask(__name__)

QUOTES = [
    "The only limit to our realization of tomorrow is our doubts of today.",
    "Adventure is worthwhile in itself.",
    "In the middle of difficulty lies opportunity.",
    "Keep calm and code on.",
    "When the going gets tough, the tough get coding."
]

@app.route("/", methods=["GET"])
def quote():
    return random.choice(QUOTES)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
