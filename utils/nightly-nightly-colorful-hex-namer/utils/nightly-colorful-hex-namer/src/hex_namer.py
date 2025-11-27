'''hex_namer.py

Provides a simple mapping from hex colour codes to whimsical names.
'''

from __future__ import annotations
import sys
import re
from typing import Tuple

# Small handcrafted palette of (RGB, name) tuples
_PALETTE = [
    ((255, 0, 0), "Crimson Fury"),
    ((0, 255, 0), "Emerald Whisper"),
    ((0, 0, 255), "Sapphire Dream"),
    ((255, 255, 0), "Solar Flare"),
    ((255, 165, 0), "Orange Ember"),
    ((128, 0, 128), "Mystic Violet"),
    ((255, 192, 203), "Blush Parade"),
    ((0, 255, 255), "Aqua Sparkle"),
    ((255, 105, 180), "Pink Pulse"),
    ((0, 128, 128), "Teal Tide"),
    ((165, 42, 42), "Rusty Relic"),
    ((255, 255, 255), "Pure Snow"),
]


def _hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    """Convert a hex colour string to an (R, G, B) tuple.

    Accepts strings with or without a leading '#'. Raises ``ValueError`` for
    malformed input.
    """
    hex_code = hex_code.strip().lstrip('#')
    if not re.fullmatch(r'[0-9a-fA-F]{6}', hex_code):
        raise ValueError(f"Invalid hex colour: {hex_code}")
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    return r, g, b


def _distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> int:
    """Euclidean distance squared between two RGB colours.
    Using the squared distance avoids a costly ``sqrt`` while preserving ordering.
    """
    return sum((a - b) ** 2 for a, b in zip(c1, c2))


def name_from_hex(hex_code: str) -> str:
    """Return the whimsical name that best matches the supplied hex colour.

    If the colour exactly matches an entry in the palette, that name is returned.
    Otherwise the nearest colour (by Euclidean distance) is chosen.
    """
    rgb = _hex_to_rgb(hex_code)
    best_name: str | None = None
    best_dist: int | None = None
    for palette_rgb, name in _PALETTE:
        dist = _distance(rgb, palette_rgb)
        if best_dist is None or dist < best_dist:
            best_dist = dist
            best_name = name
    # ``best_name`` is guaranteed to be set because the palette is non‑empty.
    return best_name  # type: ignore


def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.hex_namer \"#RRGGBB\"")
        sys.exit(1)
    try:
        print(name_from_hex(sys.argv[1]))
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    _cli()
