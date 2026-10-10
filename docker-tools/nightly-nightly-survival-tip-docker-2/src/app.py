import random
from flask import Flask, jsonify

app = Flask(__name__)

TIPS = [
    "Always carry a rubber duck for morale.",
    "If you hear a howl, it's probably just the wind.",
    "Never trust a cactus with your secrets.",
    "A well‑timed joke can defuse a mutant ambush.",
    "Remember: sunscreen works on radiation too."
]

def get_random_tip():
    """Return a random tip from TIPS."""
    return random.choice(TIPS)

@app.route("/tip")
def tip():
    return jsonify({"tip": get_random_tip()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
