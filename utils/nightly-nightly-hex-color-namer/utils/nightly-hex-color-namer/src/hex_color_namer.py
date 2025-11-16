#!/usr/bin/env python3
"""hex_color_namer

Provides a function to map a hex colour string to the nearest colour name
from a small built‑in palette.
"""
import sys
import re
from typing import Tuple, Dict

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
    """Parse a ``#RRGGBB`` string into an ``(r, g, b)`` tuple.

    Raises:
        ValueError: If the input is not a valid 6‑digit hex colour.
    """
    match = HEX_RE.fullmatch(hex_code.strip())
    if not match:
        raise ValueError(f"Invalid hex color: {hex_code}")
    hex_val = match.group(1)
    r = int(hex_val[0:2], 16)
    g = int(hex_val[2:4], 16)
    b = int(hex_val[4:6], 16)
    return r, g, b


def _distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
    """Euclidean distance between two RGB colours."""
    return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2) ** 0.5


def hex_to_name(hex_code: str) -> str:
    """Return the name of the palette colour closest to *hex_code*.

    The function is deterministic and offline – it relies solely on the
    hard‑coded ``PALETTE``.
    """
    target = _parse_hex(hex_code)
    closest_name = min(PALETTE, key=lambda name: _distance(target, PALETTE[name]))
    return closest_name


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.hex_color_namer <hex_code>", file=sys.stderr)
        sys.exit(1)
    try:
        name = hex_to_name(sys.argv[1])
        print(name)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
