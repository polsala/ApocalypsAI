import datetime
from flask import Flask, jsonify

app = Flask(__name__)

def get_hour():
    """Return the current hour in 24‑hour format. Separated for easy testing."""
    return datetime.datetime.now().hour

def select_emoji(hour):
    if 5 <= hour <= 11:
        return "🌞"
    if 12 <= hour <= 17:
        return "☕"
    if 18 <= hour <= 21:
        return "🌙"
    return "⭐"

@app.route("/mood")
def mood():
    hour = get_hour()
    return jsonify({"emoji": select_emoji(hour)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
