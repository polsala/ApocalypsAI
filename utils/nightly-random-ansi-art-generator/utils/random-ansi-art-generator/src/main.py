#!/usr/bin/env python3
"""
random-ansi-art-generator

Generates a rectangular block of random ANSI colors.
"""

import argparse
import random
from typing import List

# ANSI color codes for foreground 30-37 and background 40-47
FG_COLORS = [30, 31, 32, 33, 34, 35, 36, 37]
BG_COLORS = [40, 41, 42, 43, 44, 45, 46, 47]
BLOCK_CHAR = "█"


def _ansi_code(fg: int, bg: int) -> str:
    return f"\x1b[{fg};{bg}m{BLOCK_CHAR}\x1b[0m"


def generate_art(width: int, height: int, seed: int | None = None) -> str:
    """
    Generate a string containing `height` lines of `width` colored blocks.

    Parameters
    ----------
    width: int
        Number of blocks per line.
    height: int
        Number of lines.
    seed: int | None
        Optional seed for deterministic output.

    Returns
    -------
    str
        ANSI‑colored art.
    """
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive integers")
    rnd = random.Random(seed)
    lines: List[str] = []
    for _ in range(height):
        line_chars = [_ansi_code(rnd.choice(FG_COLORS), rnd.choice(BG_COLORS)) for _ in range(width)]
        lines.append("".join(line_chars))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate random ANSI art.")
    parser.add_argument("-w", "--width", type=int, default=10, help="Width of the art (blocks per line).")
    parser.add_argument("-t", "--height", type=int, default=5, help="Height of the art (lines).")
    parser.add_argument("-s", "--seed", type=int, default=None, help="Random seed for reproducible output.")
    args = parser.parse_args()
    art = generate_art(args.width, args.height, args.seed)
    print(art)


if __name__ == "__main__":
    main()
