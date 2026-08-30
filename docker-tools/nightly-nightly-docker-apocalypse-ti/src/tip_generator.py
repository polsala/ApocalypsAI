#!/usr/bin/env python3
import sys
import random
import time

TIPS = [
    "Always keep a spare can‑of‑beans in your bunker.",
    "Never trust a solar panel that smiles back.",
    "Map your routes with chalk; batteries die faster than you think.",
    "When the wind howls, sing to keep the mutants at bay.",
    "A well‑maintained radio is louder than a screaming crowd.",
    "Store water in copper; it tastes like victory.",
    "Learn to read the stars; GPS is a luxury of the past.",
    "Never leave your flashlight on; darkness is a friend, not a foe.",
    "Barter with jokes; laughter is the most stable currency.",
    "Plant a cactus; it survives the apocalypse better than you."
]

def get_tip(index: int | None = None) -> str:
    if index is None:
        # Seed with current time for randomness
        random.seed(time.time())
        index = random.randint(0, len(TIPS) - 1)
    else:
        # Clamp index to valid range
        index = max(0, min(index, len(TIPS) - 1))
    return TIPS[index]

def main():
    idx = None
    if len(sys.argv) > 1:
        try:
            idx = int(sys.argv[1])
        except ValueError:
            print("Argument must be an integer index.", file=sys.stderr)
            sys.exit(1)
    print(get_tip(idx))

if __name__ == "__main__":
    main()
