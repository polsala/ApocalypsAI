import json
from flask import Flask, jsonify

app = Flask(__name__)

# Hard‑coded whimsical survival quotes
QUOTES = [
    "When the world ends, remember: a well‑stocked pantry is the ultimate weapon.",
    "In the wasteland, a good joke is worth more than a fresh can of beans.",
    "Never trust a mutant with a smile; they probably ate your last snack.",
    "Radiation may glow, but a warm laugh never fades."
]

def get_quote() -> str:
    """Return the first quote (deterministic for testing)."""
    return QUOTES[0]

@app.route('/quote', methods=['GET'])
def quote_endpoint():
    return jsonify({"quote": get_quote()})

if __name__ == '__main__':
    # Run on host 0.0.0.0 to be reachable from Docker port mapping
    app.run(host='0.0.0.0', port=5000)
