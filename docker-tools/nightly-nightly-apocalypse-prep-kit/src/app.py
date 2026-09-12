from flask import Flask, jsonify, request
import random

app = Flask(__name__)

APOCALYPSE_SCENARIOS = {
    "zombie": {
        "description": "The undead walk among us! Prepare for shambling hordes.",
        "items": [
            "Crowbar (for cranial re-education)",
            "Canned Beans (indefinite shelf life)",
            "First-Aid Kit (for bites and scrapes)",
            "Running Shoes (sprinting is key)",
            "Water Purifier (hydration is survival)",
            "Duct Tape (fixes everything, even morale)",
            "Map of local grocery stores (pre-looted)",
            "A very loud air horn (distraction!)"
        ]
    },
    "alien_invasion": {
        "description": "Little green (or grey, or purple) men are here for our planet!",
        "items": [
            "Tin Foil Hat (for mind-probe deflection)",
            "Laser Pointer (distract their mothership)",
            "Universal Translator (wishful thinking)",
            "Camouflage Blanket (blend with the shrubbery)",
            "A copy of 'War of the Worlds' (for research)",
            "Emergency signal flares (just in case)",
            "A really good hiding spot (under the bed counts)",
            "A peace offering (e.g., a really nice rock)"
        ]
    },
    "robot_uprising": {
        "description": "Our silicon overlords have decided we're obsolete.",
        "items": [
            "EMP Device (imaginary, but we can dream)",
            "Strong Magnet (for disrupting circuits)",
            "Oil Can (lube up their joints, or yours)",
            "Disguise Kit (human suit, obviously)",
            "A wrench (for 'adjusting' their programming)",
            "A copy of Isaac Asimov's laws (for negotiation)",
            "A really big hammer (for percussive maintenance)",
            "A 'Do Not Disturb' sign (for your bunker)"
        ]
    },
    "disco_apocalypse": {
        "description": "The world is ending in a flurry of glitter and questionable fashion choices.",
        "items": [
            "Glitter Cannon (for blinding foes with fabulousness)",
            "Platform Boots (for reaching higher ground, or dance moves)",
            "Mirror Ball (reflect their disco rays)",
            "Groovy Tunes Playlist (morale booster)",
            "Polyester Jumpsuit (optimal for boogieing)",
            "A very strong pair of sunglasses (for the glare)",
            "A disco ball repair kit (priorities!)",
            "A 'Stayin' Alive' instruction manual"
        ]
    },
    "existential_dread": {
        "description": "The universe is vast and uncaring. Prepare for profound introspection.",
        "items": [
            "Weighted Blanket (for comfort in the void)",
            "Hot Cocoa Mix (comfort food for the soul)",
            "Philosophical Texts (e.g., Camus, Sartre)",
            "A very patient therapist (imaginary, but helpful)",
            "Noise-cancelling headphones (for silencing cosmic whispers)",
            "A journal (to document your despair, or epiphanies)",
            "A pet rock (for companionship)",
            "A 'meaning of life' cheat sheet (spoiler: there isn't one)"
        ]
    }
}

@app.route('/generate_kit', methods=['GET'])
def generate_kit():
    scenario_name = request.args.get('scenario', 'zombie').lower()

    if scenario_name not in APOCALYPSE_SCENARIOS:
        return jsonify({"error": f"Scenario '{scenario_name}' not found. Available scenarios: {', '.join(APOCALYPSE_SCENARIOS.keys())}"}), 404

    scenario_data = APOCALYPSE_SCENARIOS[scenario_name]
    
    # Pick 3 random items for the kit
    kit_items = random.sample(scenario_data["items"], min(3, len(scenario_data["items"])))

    response = {
        "scenario": scenario_name,
        "description": scenario_data["description"],
        "apocalypse_prep_kit": kit_items,
        "message": "Stay whimsical, stay prepared!"
    }
    return jsonify(response)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Welcome to the Pocket Apocalypse Prep-Kit! Use /generate_kit to get your survival list.",
        "usage": "/generate_kit?scenario=<scenario_name>",
        "available_scenarios": list(APOCALYPSE_SCENARIOS.keys())
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
