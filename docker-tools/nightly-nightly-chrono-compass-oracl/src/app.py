import datetime
import random
from flask import Flask, jsonify

app = Flask(__name__)

def get_daily_alignment(date_obj):
    """
    Generates a deterministic whimsical temporal alignment message for a given date.
    """
    # Use the date's ordinal value as a seed for deterministic randomness
    seed = date_obj.toordinal()
    random.seed(seed)

    themes = [
        "Temporal Flux", "Chrono-Currents", "Aetheric Echoes", "Void's Embrace",
        "Stardust Trails", "Echoing Chasms", "Quantum Ripples", "Cosmic Stillness",
        "Whispering Timelines", "Fractured Moments", "Infinite Now"
    ]
    actions = [
        "Align with", "Embrace the", "Navigate through", "Seek the wisdom of",
        "Harmonize with", "Unravel the mysteries of", "Anchor yourself in",
        "Drift gently with", "Manifest the essence of", "Decipher the patterns of"
    ]
    focus_points = [
        "Serenity", "Resilience", "Innovation", "Connection", "Adaptation",
        "Curiosity", "Perspective", "Momentum", "Tranquility", "Discovery",
        "Clarity", "Growth", "Balance", "Courage"
    ]
    whimsical_elements = [
        "Whispering Sands", "Crystalized Memories", "Stellar Blooms",
        "Temporal Labyrinths", "Echoing Voids", "Shifting Realities",
        "Glimmering Horizons", "Ancient Chronometers", "Nebulous Pathways",
        "Forgotten Echoes", "Cosmic Threads"
    ]

    alignment_theme = random.choice(themes)
    alignment_action = random.choice(actions)
    alignment_focus = random.choice(focus_points)
    alignment_element = random.choice(whimsical_elements)

    message = (
        f"Today's Temporal Alignment: {alignment_action} the {alignment_focus} "
        f"amidst the {alignment_element} of the {alignment_theme}. "
        "Let your path be guided by the unseen currents."
    )
    return message

@app.route('/align', methods=['GET'])
def align():
    """
    API endpoint to get the daily temporal alignment.
    """
    today = datetime.date.today()
    alignment_message = get_daily_alignment(today)
    return jsonify({
        "date": today.isoformat(),
        "alignment": alignment_message,
        "oracle_name": "Chrono-Compass Oracle"
    })

if __name__ == '__main__';
    # Run the Flask app, listening on all interfaces
    app.run(host='0.0.0.0', port=5000)
