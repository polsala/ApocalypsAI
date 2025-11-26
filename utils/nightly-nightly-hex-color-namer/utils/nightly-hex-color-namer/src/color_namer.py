"""hex_color_namer

Provides a deterministic, whimsical name for a given hex colour code.

Example
-------
>>> name_color('#ff5733')
'vivid ember'
"""

from __future__ import annotations
import sys
from typing import List

_ADJECTIVES: List[str] = [
    "mystic",
    "vivid",
    "silent",
    "golden",
    "crimson",
]

_NOUNS: List[str] = [
    "mist",
    "storm",
    "glow",
    "ember",
    "wave",
]


def _clean_hex(hex_code: str) -> str:
    """Return a hex string without a leading '#'.

    Raises
    ------
    ValueError
        If the string is not a valid 3 or 6‑character hexadecimal value.
    """
    hex_code = hex_code.strip().lower()
    if hex_code.startswith("#"):
        hex_code = hex_code[1:]
    if len(hex_code) not in (3, 6):
        raise ValueError(f"Invalid hex colour length: {hex_code!r}")
    # Validate characters
    if any(c not in "0123456789abcdef" for c in hex_code):
        raise ValueError(f"Invalid hex colour characters: {hex_code!r}")
    # Expand short form, e.g. 'abc' -> 'aabbcc'
    if len(hex_code) == 3:
        hex_code = "".join(c * 2 for c in hex_code)
    return hex_code


def name_color(hex_code: str) -> str:
    """Return a whimsical name for *hex_code*.

    The algorithm is deterministic and offline:

    1. Clean the hex string.
    2. Convert to an integer.
    3. Choose an adjective using ``int % len(_ADJECTIVES)``.
    4. Choose a noun using ``(int // len(_ADJECTIVES)) % len(_NOUNS)``.
    """
    cleaned = _clean_hex(hex_code)
    int_val = int(cleaned, 16)
    adj = _ADJECTIVES[int_val % len(_ADJECTIVES)]
    noun = _NOUNS[(int_val // len(_ADJECTIVES)) % len(_NOUNS)]
    return f"{adj} {noun}"


def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m utils.nightly_hex_color_namer.src.color_namer <hex>")
        sys.exit(1)
    try:
        print(name_color(sys.argv[1]))
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    _cli()
