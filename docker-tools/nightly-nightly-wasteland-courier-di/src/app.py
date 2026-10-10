from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Mock rationale: Simulating dynamic wasteland conditions without external dependencies.
# In a real scenario, this might come from a database or a real-time sensor network.
WASTELAND_HAZARDS = {
    "Sector Alpha": {"radiation": 0.8, "mutants": 0.2, "resources": 0.1},
    "Dusty Flats": {"radiation": 0.1, "mutants": 0.5, "resources": 0.3},
    "Whispering Canyons": {"radiation": 0.4, "mutants": 0.7, "resources": 0.05},
    "Oasis Haven": {"radiation": 0.05, "mutants": 0.05, "resources": 0.9},
    "Ruined City Center": {"radiation": 0.9, "mutants": 0.9, "resources": 0.01},
    "Barren Peaks": {"radiation": 0.6, "mutants": 0.3, "resources": 0.2},
}

@app.route('/optimize_route', methods=['POST'])
def optimize_route():
    data = request.get_json()
    start = data.get('start')
    end = data.get('end')
    waypoints = data.get('waypoints', [])

    if not all([start, end]):
        return jsonify({"error": "Start and end points are required."}), 400

    full_path = [start] + waypoints + [end]
    total_danger_rating = 0.0
    estimated_resource_consumption = 0.0
    path_segments = []

    for i in range(len(full_path) - 1):
        segment_start = full_path[i]
        segment_end = full_path[i+1]

        # Mock rationale: Simplified distance calculation for demonstration.
        # In a real system, this would use geographical coordinates.
        distance = random.uniform(5, 50) # Simulate distance between points

        # Mock rationale: Simulate hazard calculation based on known sectors.
        # This avoids needing a complex map or real-time hazard data.
        # If a point isn't a known sector, assign average hazard.
        start_hazard = WASTELAND_HAZARDS.get(segment_start, {"radiation": 0.5, "mutants": 0.5, "resources": 0.1})
        end_hazard = WASTELAND_HAZARDS.get(segment_end, {"radiation": 0.5, "mutants": 0.5, "resources": 0.1})

        # Whimsical danger calculation
        segment_danger = (start_hazard["radiation"] + start_hazard["mutants"] +
                          end_hazard["radiation"] + end_hazard["mutants"]) / 4.0 * distance
        total_danger_rating += segment_danger

        # Whimsical resource consumption
        segment_consumption = (distance * 0.1) + (segment_danger * 0.05) # More danger = more fuel
        estimated_resource_consumption += segment_consumption

        path_segments.append({
            "from": segment_start,
            "to": segment_end,
            "distance_units": round(distance, 2),
            "segment_danger_rating": round(segment_danger, 2),
            "segment_resource_consumption": round(segment_consumption, 2)
        })

    # Mock rationale: A truly "optimized" path would involve complex algorithms.
    # For this utility, "optimization" is presented as a summary of a given path.
    # The agent's task is to provide a *useful* tool, not necessarily a perfect one.
    # The "optimized_path" here is simply the input path, but with calculated metrics.
    optimized_path_summary = {
        "path_taken": full_path,
        "total_distance_units": round(sum(s['distance_units'] for s in path_segments), 2),
        "overall_danger_rating": round(total_danger_rating, 2),
        "estimated_total_resource_consumption": round(estimated_resource_consumption, 2),
        "detailed_segments": path_segments,
        "dispatch_advice": "Proceed with caution, courier! The wasteland is ever-changing."
    }

    return jsonify(optimized_path_summary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
