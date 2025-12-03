"""color_converter.py

Utility functions for converting between hexadecimal color strings and RGB tuples.

Both functions raise ``ValueError`` on malformed input.
"""

from __future__ import annotations
import sys
from typing import Tuple

HEX_PREFIX = "#"

def _normalize_hex(hex_str: str) -> str:
    """Return a 6‑character hex string without the leading '#'.

    Accepts forms like "#ff00aa", "ff00aa", "#F0A", or "F0A".
    """
    hex_str = hex_str.strip().lstrip(HEX_PREFIX).lower()
    if len(hex_str) == 3:
        # Expand short form, e.g. "f0a" -> "ff00aa"
        hex_str = "".join(ch * 2 for ch in hex_str)
    if len(hex_str) != 6 or any(c not in "0123456789abcdef" for c in hex_str):
        raise ValueError(f"Invalid hex color: '{hex_str}'")
    return hex_str

def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """Convert a hex color string to an ``(r, g, b)`` tuple.

    Parameters
    ----------
    hex_str: str
        Hexadecimal color, with or without a leading '#'.  Short form (3 digits) is supported.

    Returns
    -------
    tuple[int, int, int]
        Red, green, and blue components in the range 0‑255.
    """
    hex_clean = _normalize_hex(hex_str)
    r = int(hex_clean[0:2], 16)
    g = int(hex_clean[2:4], 16)
    b = int(hex_clean[4:6], 16)
    return (r, g, b)

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert an ``(r, g, b)`` tuple to a hex color string prefixed with '#'.

    Parameters
    ----------
    r, g, b: int
        Color components; must be in the range 0‑255.

    Returns
    -------
    str
        Hexadecimal representation, e.g. "#ff00aa".
    """
    for comp, name in zip((r, g, b), ("r", "g", "b")):
        if not (0 <= comp <= 255):
            raise ValueError(f"{name} component {comp} out of range 0‑255")
    return f"{HEX_PREFIX}{r:02x}{g:02x}{b:02x}"

def _cli() -> None:
    """Very small command‑line interface.

    Usage:
        python -m color_converter hex <hex_string>
        python -m color_converter rgb <r> <g> <b>
    """
    if len(sys.argv) < 3:
        print("Usage: python -m color_converter <hex|rgb> <value...>")
        sys.exit(1)
    mode = sys.argv[1].lower()
    if mode == "hex":
        try:
            rgb = hex_to_rgb(sys.argv[2])
            print(rgb)
        except ValueError as e:
            print(e)
            sys.exit(1)
    elif mode == "rgb":
        if len(sys.argv) != 5:
            print("RGB mode requires three integer components.")
            sys.exit(1)
        try:
            r, g, b = map(int, sys.argv[2:5])
            print(rgb_to_hex(r, g, b))
        except ValueError as e:
            print(e)
            sys.exit(1)
    else:
        print(f"Unknown mode '{mode}'. Use 'hex' or 'rgb'.")
        sys.exit(1)

if __name__ == "__main__":
    _cli()
