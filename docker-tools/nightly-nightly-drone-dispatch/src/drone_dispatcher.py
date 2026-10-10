import random
import time

def generate_destination():
    destinations = [
        "The Glowing Grotto", "Rustbucket Ridge", "Whispering Wastes Outpost",
        "Canyon of the Silent Echoes", "Mutant Mire Village", "The Last Oasis",
        "Scavenger's Haven", "Temporal Tear Trading Post"
    ]
    return random.choice(destinations)

def generate_cargo():
    cargo_items = [
        "10 cans of irradiated beans", "a vintage pre-fall comic book",
        "a Geiger counter (slightly broken)", "a map to a rumored clean water source",
        "a box of 'mystery meat' rations", "a solar-powered flashlight",
        "a collection of pre-fall bottle caps", "a manual for 'Advanced Wasteland Survival'"
    ]
    return random.choice(cargo_items)

def simulate_delivery(destination):
    base_time_minutes = random.randint(30, 180) # 0.5 to 3 hours
    outcome = "Successful"
    delay_reason = None
    loss_reason = None

    # Introduce random anomalies
    anomaly_chance = random.random()

    if anomaly_chance < 0.1: # 10% chance of major loss
        outcome = "Lost"
        loss_reason = random.choice([
            "Temporal distortion swallowed the drone whole.",
            "Attacked by a flock of irradiated ravens.",
            "Drone veered off course into the Acidic Swamps.",
            "EMP burst from a forgotten pre-fall satellite."
        ])
    elif anomaly_chance < 0.4: # 30% chance of delay (0.1 to 0.4)
        outcome = "Delayed"
        delay_minutes = random.randint(60, 240) # 1 to 4 hours delay
        base_time_minutes += delay_minutes
        delay_reason = random.choice([
            "Encountered unexpected radiation storm.",
            "Navigation system briefly scrambled by void whispers.",
            "Had to refuel at a precarious, abandoned gas station.",
            "Drone pilot (AI) got distracted by a shiny object."
        ])

    return outcome, base_time_minutes, delay_reason, loss_reason

def dispatch_drone():
    destination = generate_destination()
    cargo = generate_cargo()
    outcome, total_time, delay_reason, loss_reason = simulate_delivery(destination)

    report = f"--- Drone Dispatch Report ---\n"
    report += f"Dispatch Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC\n"
    report += f"Destination: {destination}\n"
    report += f"Cargo: {cargo}\n"
    report += f"Outcome: {outcome}\n"

    if outcome == "Successful":
        report += f"Estimated Travel Time: {total_time} minutes\n"
        report += f"Status: Cargo safely delivered to {destination}!\n"
    elif outcome == "Delayed":
        report += f"Estimated Travel Time (including delay): {total_time} minutes\n"
        report += f"Delay Reason: {delay_reason}\n"
        report += f"Status: Cargo is en route, but running late.\n"
    elif outcome == "Lost":
        report += f"Loss Reason: {loss_reason}\n"
        report += f"Status: Drone and cargo lost in transit. May the void have mercy.\n"
    report += "-----------------------------\n"
    return report

if __name__ == "__main__":
    print(dispatch_drone())
