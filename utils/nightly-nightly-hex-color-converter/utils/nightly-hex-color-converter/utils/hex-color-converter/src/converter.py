"""hex_color_converter
=====================

Utility module providing conversion between hexadecimal colour strings and RGB tuples.

Both functions raise ``ValueError`` on malformed input.

The module also offers a tiny CLI for interactive use.
"""

from __future__ import annotations

import argparse
import re
import sys
from typing import Tuple

_HEX_PATTERN = re.compile(r"^#?([0-9a-fA-F]{6})$")


def _validate_hex(hex_str: str) -> str:
    """Validate and normalise a hex colour string.

    Returns the six‑character lower‑case hex digits without leading ``#``.
    """
    match = _HEX_PATTERN.fullmatch(hex_str.strip())
    if not match:
        raise ValueError(f"Invalid hex colour: '{hex_str}'")
    return match.group(1).lower()


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """Convert a hex colour (e.g. ``"#ff00aa"`` or ``"ff00aa"``) to an ``(R, G, B)`` tuple.

    >>> hex_to_rgb("#ff00aa")
    (255, 0, 170)
    """
    clean = _validate_hex(hex_str)
    r = int(clean[0:2], 16)
    g = int(clean[2:4], 16)
    b = int(clean[4:6], 16)
    return (r, g, b)


def _validate_rgb_components(r: int, g: int, b: int) -> Tuple[int, int, int]:
    for comp, name in zip((r, g, b), ("R", "G", "B")):
        if not (0 <= comp <= 255):
            raise ValueError(f"{name} component {comp} out of range 0‑255")
    return (r, g, b)


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert an ``(R, G, B)`` tuple to a CSS hex string (e.g. ``"#ff00aa"``).

    >>> rgb_to_hex((255, 0, 170))
    '#ff00aa'
    """
    r, g, b = _validate_rgb_components(*rgb)
    return f"#{r:02x}{g:02x}{b:02x}"


def _cli_hex_to_rgb(args: argparse.Namespace) -> None:
    try:
        rgb = hex_to_rgb(args.hex)
        print(rgb)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


def _cli_rgb_to_hex(args: argparse.Namespace) -> None:
    try:
        rgb = (args.r, args.g, args.b)
        hex_code = rgb_to_hex(rgb)
        print(hex_code)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Convert between hex colour codes and RGB tuples.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--hex", type=str, help="Hex colour string to convert to RGB (e.g. '#ff00aa').")
    group.add_argument("--rgb", nargs=3, type=int, metavar=("R", "G", "B"), help="RGB components to convert to hex.")
    args = parser.parse_args(argv)
    if args.hex is not None:
        _cli_hex_to_rgb(args)
    else:
        # args.rgb is a list of three ints
        args.r, args.g, args.b = args.rgb
        _cli_rgb_to_hex(args)


if __name__ == "__main__":
    main()
