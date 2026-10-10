from flask import Flask, jsonify
from quote_mixer import get_mixed_quote

app = Flask(__name__)

@app.route("/quote")
def quote():
    return jsonify({"quote": get_mixed_quote()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
