"""
hex_color_namer: map hex color strings to nearest basic color names.
"""

from __future__ import annotations
import re
from typing import Tuple, Dict

# Basic palette of common colors
_PALETTE: Dict[str, Tuple[int, int, int]] = {
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

_HEX_RE = re.compile(r"^#?([0-9a-fA-F]{6})$")


def _hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    """Convert a hex string to an (R, G, B) tuple.

    Raises:
        ValueError: If ``hex_code`` is not a valid 6‑digit hex color.
    """
    m = _HEX_RE.fullmatch(hex_code.strip())
    if not m:
        raise ValueError(f"Invalid hex color: {hex_code!r}")
    hex_clean = m.group(1)
    r = int(hex_clean[0:2], 16)
    g = int(hex_clean[2:4], 16)
    b = int(hex_clean[4:6], 16)
    return r, g, b


def _distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> int:
    """Euclidean distance squared between two RGB colors."""
    return sum((a - b) ** 2 for a, b in zip(c1, c2))


def hex_to_name(hex_code: str) -> str:
    """Return the name of the nearest basic color for ``hex_code``.

    If ``hex_code`` cannot be parsed, returns ``"unknown"``.
    """
    try:
        rgb = _hex_to_rgb(hex_code)
    except ValueError:
        return "unknown"

    nearest_name, _ = min(_PALETTE.items(), key=lambda item: _distance(rgb, item[1]))
    return nearest_name


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m utils.nightly-hex-color-namer.src.color_namer <hex_code>")
        sys.exit(1)
    print(hex_to_name(sys.argv[1]))
