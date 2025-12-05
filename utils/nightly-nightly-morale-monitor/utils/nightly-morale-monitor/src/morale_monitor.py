import argparse
import os

MORALE_IMPACTS = {
    "found": 5,
    "discovered": 3,
    "lost": -4,
    "ran out": -5,
    "saw": 1,
    "heard": -2,
    "fixed": 6,
    "broke": -3,
    "shared": 7,
    "argued": -6,
    "repaired": 4,
    "damaged": -3,
    "celebrated": 8,
    "mourned": -7
}

def read_events(filepath):
    """Reads events from a specified text file, one event per line."""
    if not os.path.exists(filepath):
        print(f"Error: Events file not found at '{filepath}'")
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            events = [line.strip() for line in f if line.strip()]
        return events
    except IOError as e:
        print(f"Error reading events file '{filepath}': {e}")
        return []

def calculate_morale(events):
    """Calculates the total morale score based on a list of events."""
    total_morale = 0
    for event in events:
        event_lower = event.lower()
        for keyword, impact in MORALE_IMPACTS.items():
            if keyword in event_lower:
                total_morale += impact
                # Only count the first matching keyword per event to avoid double-counting
                break 
    return total_morale

def generate_report(morale_score):
    """Generates a whimsical report based on the morale score."""
    status_message = ""
    if morale_score >= 15:
        status_message = "Morale: **Radiant!** The wasteland is practically sparkling with good vibes. Keep that energy flowing, survivors!"
    elif morale_score >= 5:
        status_message = "Morale: **Optimistic Glow.** Things are looking up! A few more wins and we'll be practically skipping through the rubble."
    elif morale_score >= -4:
        status_message = "Morale: **Holding Steady.** Not great, not terrible. Just another day in the apocalypse. Keep calm and carry on... or scavenge."
    else:
        status_message = "Morale: **A Bit Grimy.** The gloom is setting in. Time for a morale-boosting scavenger hunt, or perhaps a sing-along to a pre-apocalypse pop hit?"

    report = f"""
--- Nightly Morale Report ---

{status_message}

Total Morale Score: {morale_score}

-----------------------------
"""
    return report

def main():
    parser = argparse.ArgumentParser(
        description="Calculate and report on community morale based on daily events."
    )
    parser.add_argument(
        "--events",
        type=str,
        default="daily_events.txt",
        help="Path to the text file containing daily events (one per line)."
    )
    args = parser.parse_args()

    events = read_events(args.events)
    if not events:
        print("No events to process. Morale remains a mystery.")
        return

    morale_score = calculate_morale(events)
    report = generate_report(morale_score)
    print(report)

if __name__ == "__main__":
    main()
