import random
import datetime

MORALE_BOOSTS = [
    "Remember, even a broken clock is right twice a day. You're better than a broken clock! Keep going!",
    "Your resilience is stronger than a reinforced bunker door. Don't let the gloom get to you!",
    "The best way to predict the future is to invent it. Or at least survive it with style!",
    "Even in the darkest fallout, a single spark of hope can ignite a bonfire. Be that spark!",
    "You've survived 100% of your worst days so far. Keep that streak alive!",
    "Today's challenge is tomorrow's epic survival story. Make it a good one!",
    "Don't just survive, thrive! Even if 'thriving' means finding an extra can of beans.",
    "Your inner strength is a renewable resource. Tap into it!",
    "The only thing more persistent than a rad-roach is your will to succeed. Prove it!",
    "Keep your head up, your wits sharp, and your Geiger counter handy. You got this!",
    "Every step forward, no matter how small, is a victory against the void. Celebrate it!",
    "You're not just a survivor; you're a legend in the making. Act like one!",
]

def get_morale_boost() -> str:
    """
    Selects a random morale-boosting message.
    """
    return random.choice(MORALE_BOOSTS)

def main():
    """
    Prints a timestamped morale boost to the console.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    boost_message = get_morale_boost()
    print(f"[{timestamp}] {boost_message}")

if __name__ == "__main__":
    main()
