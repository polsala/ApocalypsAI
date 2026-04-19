import hashlib
import json
import random
import time
from datetime import datetime, timezone

from flask import Flask, request

app = Flask(__name__)

# Whimsical word lists
ADJECTIVES = [
    "Whispering", "Forgotten", "Glimmering", "Silent", "Rusting", "Veiled",
    "Echoing", "Ancient", "Shrouded", "Radiant", "Broken", "Mystic",
    "Crimson", "Azure", "Emerald", "Obsidian", "Flickering", "Stellar"
]
NOUNS = [
    "Spire", "Sentinel", "Cavern", "Nexus", "Obelisk", "Relic",
    "Conduit", "Sanctum", "Vault", "Beacon", "Portal", "Chamber",
    "Refuge", "Outpost", "Citadel", "Monolith", "Whisperwind", "Starfall"
]
SUFFIXES = [
    "of Lost Dreams", "of Forgotten Echoes", "of the Aqueduct", "of Gleaming Scraps",
    "of the Silent Watch", "of Temporal Flux", "of the Void's Embrace",
    "of the Last Light", "of the Sunken City", "of the Iron Heart",
    "of the Crystal Shard", "of the Wandering Stars", "of the Deep Earth"
]

@app.route('/generate_beacon', methods=['GET'])
def generate_beacon():
    location = request.args.get('location', '')
    purpose = request.args.get('purpose', '')

    # Use a combination of inputs and current time for a unique ID
    seed_string = f"{location}-{purpose}-{time.time()}"
    beacon_id = hashlib.sha256(seed_string.encode('utf-8')).hexdigest()

    # Generate a whimsical description, seeded for reproducible descriptions given the same ID
    random.seed(beacon_id)
    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    suffix = random.choice(SUFFIXES)
    description = f"The {adj} {noun} {suffix}"

    current_time_utc = datetime.now(timezone.utc).isoformat(timespec='seconds') + 'Z'

    response_data = {
        "id": beacon_id,
        "description": description,
        "timestamp": current_time_utc
    }

    return json.dumps(response_data), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
