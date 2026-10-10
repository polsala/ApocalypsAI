import os
import random
import uuid
from datetime import datetime

from flask import Flask, request, jsonify

app = Flask(__name__)

# Whimsical report components
SIGNAL_STRENGTHS = ["Faint", "Moderate", "Strong", "Barely a flicker", "Resounding"]
ATMOSPHERIC_CONDITIONS = [
    "clear skies", "a light dust storm", "heavy irradiated fog",
    "a temporal ripple", "the whispers of the void", "a flock of mutated pigeons"
]
FLARE_COLORS = ["crimson", "emerald", "azure", "smoky grey", "iridescent violet"]
FLARE_TRAJECTORIES = [
    "pierced the twilight", "arced gracefully over the ruins",
    "shot skyward with a defiant hiss", "meandered slightly off-course",
    "exploded prematurely into a shower of sparks"
]
RESPONSE_TIMES = [
    "Expect a response in 1-3 solar cycles, or when the wind changes.",
    "A reply might arrive with the next trading caravan, or never.",
    "Keep your comms open; a reply could be instantaneous, or geological.",
    "The message is sent. The universe will decide when, or if, it responds."
]

@app.route('/dispatch_flare', methods=['POST'])
def dispatch_flare():
    data = request.get_json()
    if not data or 'message' not in data or 'sector' not in data:
        return jsonify({"error": "Missing 'message' or 'sector' in request body."}), 400

    message = data['message']
    sector = data['sector']

    transmission_id = f"FLARE-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
    signal_strength = random.choice(SIGNAL_STRENGTHS)
    flare_color = random.choice(FLARE_COLORS)
    flare_trajectory = random.choice(FLARE_TRAJECTORIES)
    atmospheric_condition = random.choice(ATMOSPHERIC_CONDITIONS)
    estimated_arrival_time_s = random.randint(60, 300) # Simulate 1-5 minutes

    report = (
        f"A shimmering {flare_color} flare {flare_trajectory}, carrying your plea. "
        f"Atmospheric interference was caused by {atmospheric_condition}, "
        f"but the message appears to have reached the general vicinity of {sector}. "
        f"{random.choice(RESPONSE_TIMES)}"
    )

    return jsonify({
        "status": "Flare Dispatched",
        "transmission_id": transmission_id,
        "target_sector": sector,
        "message_sent": message,
        "report": report,
        "signal_strength": signal_strength,
        "estimated_arrival_time_s": estimated_arrival_time_s
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
