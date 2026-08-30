import random
from flask import Flask, request, jsonify

app = Flask(__name__)

TIPS = [
    "Always keep a spare bottle of water.",
    "A well-placed mirror can signal for help.",
    "Never trust a quiet night in the wasteland.",
    "Carry a multi-tool; you never know when you'll need a screwdriver.",
    "Remember: the best camouflage is blending in with the dust."
]

@app.route("/tip")
def tip():
    scenario = request.args.get("scenario", "unknown")
    chosen = random.choice(TIPS)
    return jsonify({"tip": chosen, "scenario": scenario})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
