#!/usr/bin/env python3
"""
nightly-hex-color-namer

Provides a function to map a hex color string to the nearest common color name.
"""

import argparse
import re
import sys
from typing import Tuple, Dict

# Basic palette of 16 colors
PALETTE: Dict[str, Tuple[int, int, int]] = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "lime": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "silver": (192, 192, 192),
    "gray": (128, 128, 128),
    "maroon": (128, 0, 0),
    "olive": (128, 128, 0),
    "green": (0, 128, 0),
    "purple": (128, 0, 128),
    "teal": (0, 128, 128),
    "navy": (0, 0, 128),
}

HEX_RE = re.compile(r"^#?([0-9a-fA-F]{6})$")


def _parse_hex(hex_code: str) -> Tuple[int, int, int]:
    """Convert a hex string to an (R, G, B) tuple.

    Raises:
        ValueError: If the input is not a valid 6‑digit hex color.
    """
    match = HEX_RE.fullmatch(hex_code.strip())
    if not match:
        raise ValueError(f"Invalid hex color: {hex_code!r}")
    hex_clean = match.group(1)
    r = int(hex_clean[0:2], 16)
    g = int(hex_clean[2:4], 16)
    b = int(hex_clean[4:6], 16)
    return r, g, b


def _distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> int:
    """Euclidean distance squared between two RGB colors."""
    return sum((a - b) ** 2 for a, b in zip(c1, c2))


def get_color_name(hex_code: str) -> str:
    """Return the name of the nearest color from the built‑in palette.

    If the exact color exists in the palette, its name is returned.
    Otherwise the nearest color by Euclidean distance is chosen.
    """
    target = _parse_hex(hex_code)
    # Direct match
    for name, rgb in PALETTE.items():
        if rgb == target:
            return name
    # Find nearest
    nearest = min(PALETTE.items(), key=lambda item: _distance(target, item[1]))
    return nearest[0]


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Map a hex color to the nearest common color name."
    )
    parser.add_argument(
        "hex",
        help="Hex color code (e.g., #ff00ff or ff00ff).",
    )
    args = parser.parse_args()
    try:
        name = get_color_name(args.hex)
        print(name)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
