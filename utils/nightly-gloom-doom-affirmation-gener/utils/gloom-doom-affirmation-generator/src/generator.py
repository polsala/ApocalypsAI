import random

AFFIRMATIONS = [
    "Even if the world ends, your coffee machine might still work. Keep hope alive!",
    "Today's forecast: 100% chance of *something* happening. Make it good.",
    "Remember, even a broken clock is right twice a day. You're better than a broken clock.",
    "The only thing stopping you is... well, probably a giant mutant. But besides that, nothing!",
    "Your resilience is stronger than any irradiated cockroach. Probably.",
    "Don't just survive, thrive! Or at least, try not to trip over the rubble.",
    "Another day, another opportunity to not get eaten by a zombie. You're doing great!",
    "The future is unwritten, mostly because all the pens melted. But you can still write your own story!",
    "Embrace the chaos. It's just life's way of saying, 'Surprise!'"
]

def get_affirmation() -> str:
    """
    Returns a random, slightly sarcastic, yet uplifting affirmation.
    """
    if not AFFIRMATIONS:
        return "No affirmations found. Perhaps the apocalypse got them all."
    return random.choice(AFFIRMATIONS)

def main():
    """
    Prints a daily affirmation to the console.
    """
    print("✨ Your daily dose of existential dread, served with a side of hope:")
    print(f"\"{get_affirmation()}\"")

if __name__ == "__main__":
    main()
