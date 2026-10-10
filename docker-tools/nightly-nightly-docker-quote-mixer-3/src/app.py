import random
from flask import Flask, jsonify

app = Flask(__name__)

inspirational = [
    "The only limit is your mind.",
    "Dream big, act bigger.",
    "Every sunrise is a new beginning."
]

apocalyptic = [
    "as the sky cracks open.",
    "while the earth trembles.",
    "when the stars fall."
]

def mix_quote():
    return f"{random.choice(inspirational)} {random.choice(apocalyptic)}"

@app.route("/quote")
def quote():
    return jsonify({"quote": mix_quote()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
