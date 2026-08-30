import datetime
import random
import logging
from flask import Flask, jsonify, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

WHISPERS_FROM_THE_VOID = [
    "The past is a ripple, the future a wave. Ride the now.",
    "Time is not a river, but a vast, shimmering ocean.",
    "Seek not the hour, but the rhythm of the cosmos.",
    "Every tick is a choice, every tock an echo.",
    "The void whispers secrets only to those who listen beyond the clock.",
    "Synchronicity is the universe's subtle nod.",
    "Even in chaos, a hidden cadence persists.",
    "The true time is felt, not measured.",
    "What was, what is, what will be... all are now.",
    "Beware the temporal drift; it steals moments unseen."
]

STABILITY_STATUSES = [
    (0.0, 0.2, "Temporal fabric is fraying! Seek shelter!"),
    (0.2, 0.4, "Significant temporal flux detected. Proceed with caution."),
    (0.4, 0.6, "Minor temporal anomalies present. Keep an eye on your chronometers."),
    (0.6, 0.8, "Stable as a pre-collapse clockwork. All clear."),
    (0.8, 1.0, "Unusually high temporal coherence. A good day for planning!")
]

def get_stability_status(reading):
    for lower, upper, status in STABILITY_STATUSES:
        if lower <= reading <= upper:
            return status
    return "Unknown temporal state." # Should not happen with 0-1 range

@app.route('/time', methods=['GET'])
def get_community_time():
    current_utc = datetime.datetime.utcnow().isoformat() + 'Z'
    stability_reading = round(random.uniform(0.0, 1.0), 2)
    stability_status = get_stability_status(stability_reading)

    return jsonify({
        "community_consensus_time_utc": current_utc,
        "temporal_stability_reading": stability_reading,
        "stability_status": stability_status
    })

@app.route('/whisper', methods=['GET'])
def get_whisper():
    whisper = random.choice(WHISPERS_FROM_THE_VOID)
    return jsonify({"whisper": whisper})

@app.route('/report_time', methods=['POST'])
def report_time():
    data = request.get_json()
    if not data or 'local_time' not in data or 'source' not in data:
        return jsonify({"error": "Missing 'local_time' or 'source' in request body."}), 400

    local_time = data['local_time']
    source = data['source']
    logging.info(f"Received time report from {source}: {local_time}")

    return jsonify({
        "status": "Time observation logged.",
        "received_time": local_time,
        "source": source
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
