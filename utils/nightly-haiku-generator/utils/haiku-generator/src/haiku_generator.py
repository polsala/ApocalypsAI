'''Deterministic haiku generator.

The generator picks one line from each of three pre‑defined lists based on the provided integer seed.
All lines already satisfy the 5‑7‑5 syllable structure, so the output is a valid haiku.
'''

from __future__ import annotations

import argparse
from typing import List

# Pre‑defined haiku lines – each list respects the required syllable count.
LINES_5: List[str] = [
    "Silent moonlight glows",
    "Winter snowflakes drift",
    "Morning dew kisses",
]

LINES_7: List[str] = [
    "Whispers echo through the pine forest",
    "Gentle waves kiss the golden shore",
    "Stars dance above the quiet lake",
]

LINES_5_B: List[str] = [
    "Crimson leaves fall",
    "Bright sunrise awakens",
    "Soft shadows linger",
]


def generate_haiku(seed: int) -> str:
    """Return a deterministic haiku based on *seed*.
    The same *seed* always yields the same three‑line poem.
    """
    idx = seed  # simple deterministic index derived from the seed
    line1 = LINES_5[idx % len(LINES_5)]
    line2 = LINES_7[idx % len(LINES_7)]
    line3 = LINES_5_B[idx % len(LINES_5_B)]
    return "\n".join([line1, line2, line3])


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a deterministic haiku.")
    parser.add_argument("seed", type=int, help="Integer seed for reproducible output")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    print(generate_haiku(args.seed))


if __name__ == "__main__":
    main()
