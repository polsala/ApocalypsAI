"""hex_color_namer
===================

Provides a deterministic mapping from a 6‑digit hexadecimal color code to a short,
apocalyptic‑themed name.

The module can be used as a library via :func:`name_color` or as a tiny CLI.
"""

from __future__ import annotations

import argparse
import re
from typing import Dict

# ---------------------------------------------------------------------------
# Mapping table – a curated, whimsical palette.
# ---------------------------------------------------------------------------
_COLOR_MAP: Dict[str, str] = {
    "ff4500": "Molten Ember",
    "ff0000": "Crimson Cataclysm",
    "8b0000": "Blood Tide",
    "ffd700": "Solar Scorch",
    "ffa500": "Inferno Glow",
    "ff69b4": "Radiant Ruin",
    "800080": "Violet Void",
    "4b0082": "Abyssal Indigo",
    "0000ff": "Oceanic Oblivion",
    "00ffff": "Cyan Cataclysm",
    "00ff00": "Toxic Verdure",
    "7fff00": "Lime Lament",
    "ffff00": "Yellow Yawn",
    "ffffff": "Blinding Dawn",
    "c0c0c0": "Silver Shroud",
    "808080": "Gray Gloom",
    "000000": "Midnight Maw",
    "8a2be2": "Electric Eclipse",
    "ff1493": "Neon Nightmare",
    "1e90ff": "Storm Surge",
}

_FALLBACK_NAME = "Mysterious Void"

_HEX_PATTERN = re.compile(r"^#?([0-9a-fA-F]{6})$")


def _normalize_hex(hex_code: str) -> str:
    """Validate and normalize a hex color string.

    Returns the lower‑cased six‑character hex string without a leading '#'.
    Raises ``ValueError`` if the input is malformed.
    """
    match = _HEX_PATTERN.fullmatch(hex_code.strip())
    if not match:
        raise ValueError(f"Invalid hex color: '{hex_code}'. Expected format '#RRGGBB' or 'RRGGBB'.")
    return match.group(1).lower()


def name_color(hex_code: str) -> str:
    """Return the apocalyptic name for *hex_code*.

    Parameters
    ----------
    hex_code:
        A string like ``"#ff4500"`` or ``"ff4500"``.

    Returns
    -------
    str
        The mapped name, or ``"Mysterious Void"`` if the color is unknown.
    """
    normalized = _normalize_hex(hex_code)
    return _COLOR_MAP.get(normalized, _FALLBACK_NAME)


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Map a hex color to an apocalyptic name.")
    parser.add_argument("--color", required=True, help="Hex color code (e.g., '#ff4500' or 'ff4500').")
    args = parser.parse_args()
    try:
        result = name_color(args.color)
        print(result)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    _cli()
