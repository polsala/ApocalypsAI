import random
import json
import datetime
import os

def generate_report():
    resources = [
        "scrap metal", "diluted fuel", "purified water", "ancient tech parts",
        "mutated flora samples", "intact pre-fall rations", "medical supplies"
    ]
    anomalies = [
        "temporal distortion detected", "faint energy signature", "unidentified signal source",
        "strange atmospheric phenomenon", "ghostly echo of a bygone era", "localized gravity fluctuation"
    ]

    report = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "drone_id": os.getenv("DRONE_ID", "DRONE-ALPHA-7"),
        "location": {
            "sector": random.choice(["Alpha", "Beta", "Gamma", "Delta"]),
            "grid": f"{random.randint(1, 99):02d}-{random.randint(1, 99):02d}"
        },
        "findings": []
    }

    # Decide if we find resources
    if random.random() < 0.7: # 70% chance of finding resources
        num_resources = random.randint(1, 3)
        for _ in range(num_resources):
            resource = random.choice(resources)
            quantity = random.randint(1, 10)
            report["findings"].append({"type": "resource", "item": resource, "quantity": quantity})

    # Decide if we detect anomalies
    if random.random() < 0.3: # 30% chance of detecting anomalies
        num_anomalies = random.randint(1, 2)
        for _ in range(num_anomalies):
            anomaly = random.choice(anomalies)
            report["findings"].append({"type": "anomaly", "description": anomaly})

    if not report["findings"]:
        report["findings"].append({"type": "status", "description": "No significant findings, routine patrol."})

    return json.dumps(report, indent=2)

if __name__ == "__main__":
    print(generate_report())
