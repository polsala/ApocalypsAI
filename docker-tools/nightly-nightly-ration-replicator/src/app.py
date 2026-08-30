from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# In-memory storage for rations (for simplicity, not persistent across restarts)
rations = []

# Whimsical facts
whimsical_facts = [
    "A single can of irradiated peaches provides enough morale boost to survive an extra 3.14 hours in a zombie horde!",
    "Consuming dehydrated algae wafers can improve your night vision, crucial for scavenging under the twin moons.",
    "This nutrient paste, while bland, contains the essential elements to resist temporal displacement for up to 72 hours.",
    "Remember, a well-hydrated survivor is a less-grumpy survivor. Drink your reclaimed rainwater!",
    "The caloric density of a mutated squirrel leg is surprisingly high, offering peak energy for quick escapes.",
    "Emergency chocolate rations are not just for energy; they're vital for maintaining sanity in the desolate wastes.",
    "A balanced diet of scavenged roots and grubs can extend your lifespan by approximately 0.02% per day!",
    "Beware of glowing berries; while they might look appealing, their nutritional value is often inversely proportional to their luminescence."
]

@app.route('/')
def home():
    return "Welcome to the Nightly Ration Replicator! Use /rations to manage your supplies, /fact for wisdom, and /expiry for alerts."

@app.route('/rations', methods=['GET', 'POST'])
def manage_rations():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(k in data for k in ['name', 'quantity', 'expiry', 'calories_per_unit']):
            return jsonify({"error": "Missing data. Required: name, quantity, expiry (YYYY-MM-DD), calories_per_unit"}), 400
        
        try:
            # Validate expiry date format
            datetime.strptime(data['expiry'], '%Y-%m-%d')
            data['quantity'] = int(data['quantity'])
            data['calories_per_unit'] = int(data['calories_per_unit'])
            if data['quantity'] <= 0 or data['calories_per_unit'] < 0:
                raise ValueError("Quantity and calories must be positive.")
        except ValueError as e:
            return jsonify({"error": f"Invalid data format or value: {e}"}), 400

        rations.append(data)
        return jsonify({"message": "Ration added successfully", "ration": data}), 201
    else: # GET
        return jsonify(rations)

@app.route('/fact', methods=['GET'])
def get_fact():
    return jsonify({"fact": random.choice(whimsical_facts)})

@app.route('/expiry', methods=['GET'])
def check_expiry():
    days_param = request.args.get('days', type=int)
    if days_param is None or days_param <= 0:
        return jsonify({"error": "Please provide a positive 'days' parameter (e.g., /expiry?days=30)"}), 400

    today = datetime.now().date()
    expiry_threshold = today + timedelta(days=days_param)

    expiring_soon = []
    for ration in rations:
        try:
            ration_expiry_date = datetime.strptime(ration['expiry'], '%Y-%m-%d').date()
            if today <= ration_expiry_date <= expiry_threshold:
                expiring_soon.append(ration)
        except ValueError:
            # Log or handle invalid date format in stored data if necessary
            pass 
            
    return jsonify(expiring_soon)

if __name__ == '__main__':
    # For local development without Gunicorn
    app.run(debug=True, host='0.0.0.0', port=8080)
