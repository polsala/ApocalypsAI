"""hex colour generator utility

Provides:
- `generate_color(seed: int | None = None) -> str`
- `classify_brightness(hex_color: str) -> str`
- CLI entry point when executed as a module
"""

import argparse
import random
import sys
from typing import Tuple

__all__ = ["generate_color", "classify_brightness"]


def _rgb_from_ints(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """Clamp and return a tuple of RGB values (0‑255)."""
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))


def generate_color(seed: int | None = None) -> str:
    """Return a random hex colour string like ``#A1B2C3``.

    If *seed* is provided, the random generator is seeded for reproducibility.
    """
    if seed is not None:
        random.seed(seed)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    r, g, b = _rgb_from_ints(r, g, b)
    return f"#{r:02X}{g:02X}{b:02X}"


def classify_brightness(hex_color: str) -> str:
    """Classify the perceived brightness of *hex_color*.

    Returns one of ``"light"``, ``"dark"`` or ``"neutral"`` based on the
    YIQ luminance formula.
    """
    if not isinstance(hex_color, str) or not hex_color.startswith("#") or len(hex_color) != 7:
        raise ValueError("hex_color must be a string like '#A1B2C3'")
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    # YIQ luminance formula (ITU-R BT.601)
    yiq = (r * 299 + g * 587 + b * 114) / 1000
    if yiq >= 200:
        return "light"
    elif yiq <= 80:
        return "dark"
    else:
        return "neutral"


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a random hex colour code.")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional integer seed for deterministic output.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        colour = generate_color(seed=args.seed)
        brightness = classify_brightness(colour)
        print(f"{colour} ({brightness})")
        return 0
    except Exception as exc:  # pragma: no cover – defensive
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
