"""
hex_to_rgb.py

Provides a function to convert a hex colour string to an RGB tuple.
Also offers a tiny CLI for manual conversion.
"""

import sys
import re
from typing import Tuple


def _clean_hex(hex_str: str) -> str:
    """Remove leading # and whitespace, validate length.

    Args:
        hex_str: Raw hex colour string.
    Returns:
        Cleaned 6‑character lower‑case hex string.
    """
    cleaned = hex_str.strip().lstrip('#')
    if not re.fullmatch(r'[0-9a-fA-F]{6}', cleaned):
        raise ValueError(f"Invalid hex colour: '{hex_str}'")
    return cleaned.lower()


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """Convert a hex colour string to an (R, G, B) tuple.

    Args:
        hex_str: Hex colour like '#ff00aa' or 'ff00aa'.

    Returns:
        Tuple of three ints in range 0‑255.
    """
    cleaned = _clean_hex(hex_str)
    r = int(cleaned[0:2], 16)
    g = int(cleaned[2:4], 16)
    b = int(cleaned[4:6], 16)
    return (r, g, b)


def _cli():
    if len(sys.argv) != 2:
        print("Usage: python -m utils.hex_to_rgb src/hex_to_rgb.py <hex>")
        sys.exit(1)
    try:
        rgb = hex_to_rgb(sys.argv[1])
        print(rgb)
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    _cli()
