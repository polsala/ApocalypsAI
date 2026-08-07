from flask import Flask, request, jsonify

app = Flask(__name__)

# In‑memory store for radiation readings (float values)
readings = []

@app.route("/reading", methods=["POST"])
def add_reading():
    data = request.get_json()
    if not data or "value" not in data:
        return jsonify({"error": "Missing 'value'"}), 400
    try:
        val = float(data["value"])
    except (ValueError, TypeError):
        return jsonify({"error": "'value' must be a number"}), 400
    readings.append(val)
    return jsonify({"status": "ok"}), 201

@app.route("/average", methods=["GET"])
def get_average():
    if not readings:
        return jsonify({"average": None, "count": 0})
    avg = sum(readings) / len(readings)
    return jsonify({"average": avg, "count": len(readings)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
