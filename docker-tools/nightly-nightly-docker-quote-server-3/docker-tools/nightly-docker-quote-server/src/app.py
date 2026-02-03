from flask import Flask, jsonify
import random

app = Flask(__name__)

QUOTES = [
    "The ashes whisper, \"Tomorrow is a myth.\"",
    "Even the sun takes a coffee break in the wasteland.",
    "Radiation is just the universe's way of adding spice.",
    "When the wind howls, it sings the lullaby of lost cities.",
    "Hope is a cactus: prickly but survives the desert."
]

@app.route("/quote")
def quote():
    return jsonify({"quote": random.choice(QUOTES)})
