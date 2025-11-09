"""
Daily Cryptic Puzzle Generator

Provides a simple function to generate a random cryptic clue.
"""

import random
from typing import Tuple

# Small built‑in database of (clue, answer) pairs.
PUZZLES = [
    ("Day star (3)", "SUN"),
    ("Feline's sound (3)", "MEW"),
    ("Opposite of night (3)", "DAY"),
    ("First letter of alphabet (1)", "A"),
    ("Water's frozen form (3)", "ICE"),
]

def generate_puzzle() -> Tuple[str, str]:
    """Return a random (clue, answer) tuple."""
    clue, answer = random.choice(PUZZLES)
    return clue, answer

def main() -> None:
    clue, answer = generate_puzzle()
    print(f"Clue: {clue}")
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
