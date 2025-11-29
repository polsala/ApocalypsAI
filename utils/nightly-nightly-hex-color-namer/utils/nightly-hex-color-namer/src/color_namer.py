"""hex_color_namer

Provides a function to convert a hex colour code into a whimsical name.

The module is deliberately self‑contained – no external network calls –
so the tests can run offline.
"""

import sys
import re
import colorsys
from typing import Dict

# ---------------------------------------------------------------------------
# Built‑in lookup table (hex -> whimsical name)
# ---------------------------------------------------------------------------
_LOOKUP_TABLE: Dict[str, str] = {
    "#ff0000": "Blazing Ruby",
    "#00ff00": "Neon Lime",
    "#0000ff": "Electric Sapphire",
    "#ffff00": "Solar Flare",
    "#ff7f00": "Fiery Tangerine",
    "#7f00ff": "Mystic Amethyst",
    "#00ffff": "Aqua Whisper",
    "#ffffff": "Pure Snow",
    "#000000": "Midnight Void",
    "#808080": "Stormy Gray",
}

# Generic hue buckets for fallback names (ordered by hue angle)
_GENERIC_NAMES = [
    "Crimson Dawn",
    "Sunset Orange",
    "Lemon Zest",
    "Spring Green",
    "Ocean Blue",
    "Violet Dream",
    "Rose Pink",
    "Cool Cyan",
    "Warm Amber",
    "Deep Indigo",
]

_HEX_PATTERN = re.compile(r"^#?[0-9a-fA-F]{6}$")


def _normalize_hex(hex_code: str) -> str:
    """Return a lower‑case hex string prefixed with '#'."""
    hex_code = hex_code.strip().lower()
    if not hex_code.startswith("#"):
        hex_code = f"#{hex_code}"
    return hex_code


def _hue_to_generic_name(hue: float) -> str:
    """Map a hue (0‑1) to one of the generic names.

    The hue circle is split evenly among the entries in ``_GENERIC_NAMES``.
    """
    index = int(hue * len(_GENERIC_NAMES)) % len(_GENERIC_NAMES)
    return _GENERIC_NAMES[index]


def get_color_name(hex_code: str) -> str:
    """Return a whimsical name for *hex_code*.

    If *hex_code* is present in the built‑in lookup table, the associated name
    is returned. Otherwise a deterministic name based on the colour's hue is
    generated.

    Parameters
    ----------
    hex_code: str
        A 6‑digit hexadecimal colour, with or without a leading '#'.

    Returns
    -------
    str
        Whimsical colour name.
    """
    if not _HEX_PATTERN.match(hex_code):
        raise ValueError(f"Invalid hex colour: {hex_code}")

    normalized = _normalize_hex(hex_code)
    if normalized in _LOOKUP_TABLE:
        return _LOOKUP_TABLE[normalized]

    # Fallback: compute hue and map to a generic name
    r = int(normalized[1:3], 16) / 255.0
    g = int(normalized[3:5], 16) / 255.0
    b = int(normalized[5:7], 16) / 255.0
    hue, _, _ = colorsys.rgb_to_hsv(r, g, b)
    return _hue_to_generic_name(hue)


def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.color_namer <hex_code>")
        sys.exit(1)
    try:
        name = get_color_name(sys.argv[1])
        print(name)
    except ValueError as exc:
        print(str(exc))
        sys.exit(1)


if __name__ == "__main__":
    _cli()
