import argparse
import random
import sys
from datetime import datetime

def get_nudge_message(category: str = "random") -> str:
    """
    Generates a whimsical nourishment nudge message based on category.
    """
    messages = {
        "hydrate": [
            "Hydration Protocol Initiated: Remember to refuel your internal reservoirs!",
            "Warning: Desiccation detected! Grab some H2O, survivor!",
            "Your organic systems require liquid sustenance. Drink water!",
            "Don't let your circuits fry! A glass of water awaits.",
            "Recharge your internal power cells with some refreshing liquid!",
        ],
        "snack": [
            "Energy Reserves Low: Seek out a delicious, non-radioactive snack!",
            "Fueling Station Open: Time for a quick bite to keep the apocalypse at bay!",
            "Your brain-matter requires caloric input. Find a snack!",
            "A small treat can make a big difference. Snack time!",
            "Don't run on fumes! Grab a bite and keep going.",
        ],
        "break": [
            "System Overload Imminent: Initiate short break protocol!",
            "Rubble-Rousing is tiring work. Step away from the screen for a moment!",
            "Even the most resilient survivors need a pause. Take a break!",
            "Reboot your focus: a quick break can clear the cache.",
            "Stretch those weary limbs! A short break is essential for survival.",
        ],
    }

    if category == "random":
        all_messages = [msg for sublist in messages.values() for msg in sublist]
        return random.choice(all_messages)
    elif category in messages:
        return random.choice(messages[category])
    else:
        return f"Unknown nourishment category: '{category}'. Please choose from 'hydrate', 'snack', 'break', or 'random'."

def main():
    parser = argparse.ArgumentParser(
        description="Provides a whimsical nourishment nudge message."
    )
    parser.add_argument(
        "--category",
        "-c",
        choices=["hydrate", "snack", "break", "random"],
        default="random",
        help="Specify the category of nourishment nudge (default: random).",
    )
    args = parser.parse_args()

    message = get_nudge_message(args.category)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Nudge: {message}")

if __name__ == "__main__":
    main()
