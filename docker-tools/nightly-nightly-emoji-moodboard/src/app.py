import datetime
from flask import Flask, jsonify

app = Flask(__name__)

EMOJI_MAP = {
    range(0, 6): ["🌙", "😴"],
    range(6, 12): ["☕", "🌅", "😊"],
    range(12, 18): ["☀️", "😎", "🍹"],
    range(18, 24): ["🌆", "🌙", "🍷"]
}

def get_emoji_for_hour(hour: int):
    for hour_range, emojis in EMOJI_MAP.items():
        if hour in hour_range:
            return emojis
    return ["❓"]

@app.route("/mood")
def mood():
    now = datetime.datetime.utcnow()
    hour = now.hour
    emojis = get_emoji_for_hour(hour)
    return jsonify({"hour": hour, "emoji": emojis})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
