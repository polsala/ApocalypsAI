import os
from flask import Flask, jsonify

app = Flask(__name__)

mixed_quotes = [
    "The only limit to our realization of tomorrow is our doubts of today. The sky is falling, but the coffee is still hot.",
    "Believe you can and you're halfway there. When the world ends, make sure you have a good playlist."
]

def get_quote():
    # Deterministic for simplicity
    return mixed_quotes[0]

@app.route("/quote")
def quote():
    return jsonify({"quote": get_quote()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
