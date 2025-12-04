"""nightly-apocalypse-color-namer
===================================

Utility to convert a hex colour code into a whimsical, post‑apocalyptic name.

The implementation is deliberately lightweight and deterministic – it does not
require any external services or heavy dependencies.

Example
-------
>>> name_color('#ff5733')
'Radiant Wasteland'
"""

from __future__ import annotations

import re
from typing import Tuple

# ---------------------------------------------------------------------------
# Deterministic word lists – feel free to extend them in the future.
# ---------------------------------------------------------------------------
_ADJECTIVES = [
    "Radiant",
    "Moldy",
    "Blazing",
    "Frosted",
    "Toxic",
    "Dusty",
    "Glowing",
    "Ashen",
]

_NOUNS = [
    "Wasteland",
    "Radiation",
    "Salvage",
    "Cinder",
    "Bunker",
    "Scavenger",
    "Vault",
    "Ruin",
]

_HEX_PATTERN = re.compile(r"^#?[0-9a-fA-F]{6}$")


def _validate_hex(hex_code: str) -> str:
    """Validate and normalise a hex colour string.

    Parameters
    ----------
    hex_code: str
        The colour code supplied by the user (e.g. "#ff00ff" or "ff00ff").

    Returns
    -------
    str
        Normalised six‑character lower‑case hex string without a leading '#'.

    Raises
    ------
    ValueError
        If the input does not match the required pattern.
    """
    if not isinstance(hex_code, str):
        raise ValueError("hex_code must be a string")
    if not _HEX_PATTERN.match(hex_code):
        raise ValueError(f"Invalid hex colour: {hex_code!r}")
    # Strip leading '#', lower‑case for consistency.
    return hex_code.lstrip("#").lower()


def _pick_words(value: int) -> Tuple[str, str]:
    """Deterministically pick an adjective and a noun from the integer value.

    The algorithm uses simple modulo arithmetic to ensure repeatability.
    """
    adj_index = value % len(_ADJECTIVES)
    noun_index = (value // len(_ADJECTIVES)) % len(_NOUNS)
    return _ADJECTIVES[adj_index], _NOUNS[noun_index]


def name_color(hex_code: str) -> str:
    """Return a whimsical post‑apocalyptic name for a hex colour.

    Parameters
    ----------
    hex_code: str
        Hex colour string (e.g. "#ff5733" or "ff5733").

    Returns
    -------
    str
        A name such as "Radiant Wasteland".
    """
    normalised = _validate_hex(hex_code)
    numeric = int(normalised, 16)
    adjective, noun = _pick_words(numeric)
    return f"{adjective} {noun}"


def _cli() -> None:
    """Simple command‑line interface for manual testing.

    Usage:
        python -m utils.nightly-apocalypse-color-namer.src.color_namer "#ff5733"
    """
    import argparse
    parser = argparse.ArgumentParser(description="Convert a hex colour to a post‑apocalyptic name.")
    parser.add_argument("hex_code", help="Hex colour code (e.g. #ff5733)")
    args = parser.parse_args()
    try:
        print(name_color(args.hex_code))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    _cli()
