from flask import Flask, request, jsonify

app = Flask(__name__)

def classify_debris(description):
    """Classifies a given debris description into a whimsical category."""
    description_lower = description.lower()

    if any(keyword in description_lower for keyword in ["time", "past", "future", "echo", "loop", "temporal", "chronal"]):
        return {
            "category": "Temporal Fragment",
            "whimsical_name": "Chronal Shardlet",
            "survival_tip": "Beware of paradoxes! This fragment might show you yesterday's lunch, but won't bring it back."
        }
    elif any(keyword in description_lower for keyword in ["slime", "goo", "viscous", "pulsating", "unknown", "gelatinous", "amorphous"]):
        return {
            "category": "Eldritch Goo",
            "whimsical_name": "Amorphous Blob of Whispers",
            "survival_tip": "Do not taste it. Do not poke it. If it whispers, politely ask it for lottery numbers, then run."
        }
    elif any(keyword in description_lower for keyword in ["star", "crystal", "gem", "light", "radiant", "shimmering", "celestial", "splinter"]):
        return {
            "category": "Stellar Shard",
            "whimsical_name": "Harmonic Star-Splinter",
            "survival_tip": "Hold it to your ear; it might hum the location of the nearest potable water source, or just a catchy tune."
        }
    elif any(keyword in description_lower for keyword in ["dark", "void", "ancient", "whisper", "cold", "shadow", "abyssal", "relic"]):
        return {
            "category": "Void-Touched Relic",
            "whimsical_name": "Echo of the Great Nothing",
            "survival_tip": "It's probably cursed. Or a really good paperweight. Best not to find out which."
        }
    else:
        return {
            "category": "Mundane Misdirection",
            "whimsical_name": "Just a Rock (Probably)",
            "survival_tip": "It's probably just a rock. Or a very convincing piece of space junk. Still, good for throwing."
        }

@app.route('/classify', methods=['POST'])
def classify():
    """API endpoint to receive a description and return a classification."""
    data = request.get_json()
    if not data or 'description' not in data:
        return jsonify({"error": "Missing 'description' in request body"}), 400

    description = data['description']
    result = classify_debris(description)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
