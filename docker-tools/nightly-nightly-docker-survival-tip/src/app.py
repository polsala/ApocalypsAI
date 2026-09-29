import os
from flask import Flask, jsonify

app = Flask(__name__)

TIPS = [
    "Always keep a spare bottle of water in your backpack.",
    "Never trust a stranger with a shiny object.",
    "Map your routes; the wasteland changes daily.",
    "A well‑maintained radio can be your lifeline.",
    "Learn to identify edible plants; they’re everywhere."
]

def get_tip():
    try:
        idx = int(os.getenv("TIP_INDEX", "0"))
    except ValueError:
        idx = 0
    return TIPS[idx % len(TIPS)]

@app.route("/", methods=["GET"])
def tip():
    return jsonify({"tip": get_tip()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
