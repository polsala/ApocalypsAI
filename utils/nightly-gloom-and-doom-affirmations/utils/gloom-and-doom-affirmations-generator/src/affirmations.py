import random

AFFIRMATIONS = [
    "Today is a new day to survive. Or not. Either way, it's a day.",
    "My resilience is stronger than the last remaining Wi-Fi signal.",
    "I am a beacon of hope in a world that's mostly rubble. Mostly.",
    "Every sunrise is a reminder that I made it through the night. Again.",
    "My spirit is unyielding, much like this stubborn rust on my last can of beans.",
    "I embrace the chaos, for it is the only constant. And also, I have no choice.",
    "I am grateful for small mercies, like finding a non-radioactive potato.",
    "My future is bright, even if it's just the glow of distant burning cities.",
    "I am capable of adapting to any new horror the universe throws my way.",
    "The only thing more persistent than my will to live is this persistent cough."
]

def get_random_affirmation() -> str:
    """Returns a random gloom-and-doom affirmation."""
    return random.choice(AFFIRMATIONS)

def main():
    """Main function to run the utility."""
    affirmation = get_random_affirmation()
    print(f"Today's affirmation: {affirmation}")

if __name__ == "__main__":
    main()
