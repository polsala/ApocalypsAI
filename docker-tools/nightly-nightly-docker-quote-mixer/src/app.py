import random
from flask import Flask, jsonify

app = Flask(__name__)

# Inspirational quotes
INSPIRATIONAL = [
    "Your future is bright",
    "Believe in the impossible",
    "Every sunrise is a new chance",
    "Hope is the strongest weapon"
]

# Post‑apocalyptic taglines
APOCALYPTIC = [
    "The wasteland whispers your name",
    "Radiation sings lullabies",
    "Mutant crows watch over you",
    "The last bunker is opening"
]

def mix_quote() -> str:
    """Select one phrase from each list and combine them with an em dash."""
    insp = random.choice(INSPIRATIONAL)
    apo = random.choice(APOCALYPTIC)
    return f"{insp} – {apo}"

@app.route("/quote", methods=["GET"])
def get_quote():
    quote = mix_quote()
    return jsonify({"quote": quote})

if __name__ == "__main__":
    # Run on host port 8080 for Docker EXPOSE
    app.run(host="0.0.0.0", port=8080)

