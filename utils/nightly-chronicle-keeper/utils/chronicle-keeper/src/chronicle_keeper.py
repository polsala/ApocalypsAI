import os
import datetime

def generate_log_entry():
    """
    Prompts the user for daily chronicle details and generates a Markdown log file.
    """
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    filename = f"logs/{date_str}-chronicle.md"

    print(f"\n--- Chronicle Entry for {date_str} ---")

    key_events = input("Key Events (e.g., 'Scavenged Sector 7. Encountered feral drones.'):\n> ")
    resource_status = input("Resource Status (e.g., 'Food: 3 days, Water: 5 days, Ammo: 17 rounds'):\n> ")
    morale = input("Morale (1-5, 1=terrible, 5=hopeful):\n> ")
    observations = input("Observations & Reflections:\n> ")

    log_content = f"""# Chronicle Entry - {date_str}

## Key Events:

{key_events}

## Resource Status:

{resource_status}

## Morale:

{morale}/5

## Observations & Reflections:

{observations}
"""

    os.makedirs('logs', exist_ok=True)

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(log_content)
        print(f"\nChronicle entry saved to {filename}")
    except IOError as e:
        print(f"Error saving chronicle entry: {e}")

if __name__ == "__main__":
    generate_log_entry()
