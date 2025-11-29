import random
from typing import List

# List of whimsical survival tips
TIPS: List[str] = [
    "Always keep a spare can of beans in your bunker.",
    "Never trust a mutant with a smile.",
    "Water is life – filter it twice.",
    "A well‑charged flashlight is worth its weight in gold.",
    "Learn to start a fire with just two sticks – or a lighter.",
    "Keep a map of safe zones updated weekly.",
    "Never leave your shelter without a trusty sidekick.",
    "Remember: silence is louder than a gunshot in the wasteland.",
]

def get_random_tip() -> str:
    """Return a random tip from the TIPS list.

    The function is deliberately simple to keep the utility lightweight.
    """
    return random.choice(TIPS)

if __name__ == "__main__":
    print(get_random_tip())
