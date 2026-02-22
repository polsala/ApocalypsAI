import os
import random
from flask import Flask, jsonify

app = Flask(__name__)

QUOTES = [
    "The ash whispers, \"Keep moving.\"",
    "Even in ruins, hope sprouts like weeds.",
    "Radiation may glow, but your spirit shines brighter.",
    "When the world ends, coffee still brews.",
    "Survival tip: Never trust a silent wind."
]

def get_quote():
    index = os.getenv("QUOTE_INDEX")
    if index is not None and index.isdigit():
        i = int(index) % len(QUOTES)
        return QUOTES[i]
    return random.choice(QUOTES)

@app.route("/quote")
def quote():
    return jsonify({"quote": get_quote()})
