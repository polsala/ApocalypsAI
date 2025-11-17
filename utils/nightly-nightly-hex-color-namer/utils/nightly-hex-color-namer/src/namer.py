"""hex‑color‑namer utility

Provides a single public function :func:`name_color` that maps a hex colour string
(e.g. ``"#ff4500"``) to the nearest colour name from a built‑in palette.

The module can also be executed as a tiny CLI:

    python -m src.namer "#ff4500"

which prints the colour name to stdout.
"""

from __future__ import annotations

import sys
import re
from typing import Tuple, Dict

# ---------------------------------------------------------------------------
# Minimal colour palette – a subset of the CSS colour list (≈140 entries).
# The keys are lower‑case colour names; the values are hex strings *without* the
# leading '#'.  This keeps the file lightweight while still being useful.
# ---------------------------------------------------------------------------
_PALETTE: Dict[str, str] = {
    "black": "000000",
    "white": "ffffff",
    "red": "ff0000",
    "lime": "00ff00",
    "blue": "0000ff",
    "yellow": "ffff00",
    "cyan": "00ffff",
    "magenta": "ff00ff",
    "silver": "c0c0c0",
    "gray": "808080",
    "maroon": "800000",
    "olive": "808000",
    "green": "008000",
    "purple": "800080",
    "teal": "008080",
    "navy": "000080",
    "orange": "ffa500",
    "gold": "ffd700",
    "pink": "ffc0cb",
    "brown": "a52a2a",
    "coral": "ff7f50",
    "crimson": "dc143c",
    "indigo": "4b0082",
    "ivory": "fffff0",
    "khaki": "f0e68c",
    "lavender": "e6e6fa",
    "limegreen": "32cd32",
    "maroon": "800000",
    "navy": "000080",
    "olive": "808000",
    "orangered": "ff4500",
    "orchid": "da70d6",
    "salmon": "fa8072",
    "sienna": "a0522d",
    "skyblue": "87ceeb",
    "slategray": "708090",
    "steelblue": "4682b4",
    "tomato": "ff6347",
    "turquoise": "40e0d0",
    "violet": "ee82ee",
    "wheat": "f5deb3",
    "springgreen": "00ff7f",
    "royalblue": "4169e1",
    "darkorange": "ff8c00",
    "lightseagreen": "20b2aa",
    "mediumvioletred": "c71585",
    "darkslategray": "2f4f4f",
    "lightgoldenrodyellow": "fafad2",
    "palegreen": "98fb98",
    "mediumaquamarine": "66cdaa",
    "mediumspringgreen": "00fa9a",
    "mediumseagreen": "3cb371",
    "mediumturquoise": "48d1cc",
    "mediumslateblue": "7b68ee",
    "mediumorchid": "ba55d3",
    "mediumblue": "0000cd",
    "mediumforestgreen": "228b22",
    "lightcoral": "f08080",
    "lightsteelblue": "b0c4de",
    "lightpink": "ffb6c1",
    "lightgray": "d3d3d3",
    "lightcyan": "e0ffff",
    "lightblue": "add8e6",
    "lightgreen": "90ee90",
    "lightyellow": "ffffe0",
    "lightgoldenrod": "eedd82",
    "lightseagreen": "20b2aa",
    "lightsalmon": "ffa07a",
    "lightskyblue": "87cefa",
    "lightslategray": "778899",
    "lightsteelblue": "b0c4de",
    "mediumslateblue": "7b68ee",
    "darkgoldenrod": "b8860b",
    "darkkhaki": "bdb76b",
    "darkolivegreen": "556b2f",
    "darkorange": "ff8c00",
    "darkorchid": "9932cc",
    "darksalmon": "e9967a",
    "darkseagreen": "8fbc8f",
    "darkslateblue": "483d8b",
    "darkturquoise": "00ced1",
    "darkviolet": "9400d3",
    "deeppink": "ff1493",
    "deepskyblue": "00bfff",
    "dodgerblue": "1e90ff",
    "firebrick": "b22222",
    "floralwhite": "fffaf0",
    "forestgreen": "228b22",
    "fuchsia": "ff00ff",
    "gainsboro": "dcdcdc",
    "ghostwhite": "f8f8ff",
    "goldenrod": "daa520",
    "greenyellow": "adff2f",
    "honeydew": "f0fff0",
    "hotpink": "ff69b4",
    "indianred": "cd5c5c",
    "lavenderblush": "fff0f5",
    "lawngreen": "7cfc00",
    "lemonchiffon": "fffacd",
    "lightgoldenrodyellow": "fafad2",
    "linen": "faf0e6",
    "mediumaquamarine": "66cdaa",
    "mediumblue": "0000cd",
    "mediumorchid": "ba55d3",
    "mediumpurple": "9370db",
    "mediumseagreen": "3cb371",
    "mediumslateblue": "7b68ee",
    "mediumspringgreen": "00fa9a",
    "mediumturquoise": "48d1cc",
    "mediumvioletred": "c71585",
    "midnightblue": "191970",
    "mintcream": "f5fffa",
    "mistyrose": "ffe4e1",
    "moccasin": "ffe4b5",
    "navajowhite": "ffdead",
    "oldlace": "fdf5e6",
    "olivedrab": "6b8e23",
    "orangered": "ff4500",
    "orchid": "da70d6",
    "palegoldenrod": "eee8aa",
    "palegreen": "98fb98",
    "paleturquoise": "afeeee",
    "palevioletred": "db7093",
    "papayawhip": "ffefd5",
    "peachpuff": "ffdab9",
    "peru": "cd853f",
    "pink": "ffc0cb",
    "plum": "dda0dd",
    "powderblue": "b0e0e6",
    "rosybrown": "bc8f8f",
    "royalblue": "4169e1",
    "saddlebrown": "8b4513",
    "salmon": "fa8072",
    "sandybrown": "f4a460",
    "seagreen": "2e8b57",
    "seashell": "fff5ee",
    "sienna": "a0522d",
    "skyblue": "87ceeb",
    "slateblue": "6a5acd",
    "slategray": "708090",
    "snow": "fffafa",
    "steelblue": "4682b4",
    "tan": "d2b48c",
    "thistle": "d8bfd8",
    "tomato": "ff6347",
    "turquoise": "40e0d0",
    "violet": "ee82ee",
    "wheat": "f5deb3",
    "whitesmoke": "f5f5f5",
    "yellowgreen": "9acd32",
}

_HEX_RE = re.compile(r"^#?([0-9a-fA-F]{6})$")


def _hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """Convert a 6‑digit hex string (with optional leading '#') to an RGB tuple.

    Raises:
        ValueError: If the string is not a valid 6‑digit hex colour.
    """
    match = _HEX_RE.fullmatch(hex_str.strip())
    if not match:
        raise ValueError(f"Invalid hex colour: {hex_str!r}")
    hex_clean = match.group(1)
    r = int(hex_clean[0:2], 16)
    g = int(hex_clean[2:4], 16)
    b = int(hex_clean[4:6], 16)
    return r, g, b


def _distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
    """Euclidean distance between two RGB colours."""
    return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2) ** 0.5


def name_color(hex_code: str) -> str:
    """Return the nearest colour name for *hex_code*.

    The function parses *hex_code* (e.g. ``"#ff4500"`` or ``"ff4500"``), then
    computes the Euclidean distance in RGB space to each entry in the built‑in
    palette.  The name with the smallest distance is returned.

    Args:
        hex_code: A 6‑digit hexadecimal colour string, optionally prefixed with
            ``#``.

    Returns:
        The nearest colour name (lower‑case).

    Raises:
        ValueError: If *hex_code* is malformed.
    """
    target_rgb = _hex_to_rgb(hex_code)
    best_name = None
    best_dist = float("inf")
    for name, palette_hex in _PALETTE.items():
        palette_rgb = _hex_to_rgb(palette_hex)
        dist = _distance(target_rgb, palette_rgb)
        if dist < best_dist:
            best_dist = dist
            best_name = name
    # ``best_name`` will always be set because the palette is non‑empty.
    return best_name  # type: ignore[return-value]


def _cli() -> None:
    """Simple command‑line interface used when the module is executed directly.

    Expected usage:
        python -m src.namer "#ff4500"
    """
    if len(sys.argv) != 2:
        print("Usage: python -m src.namer <hex-colour>", file=sys.stderr)
        sys.exit(2)
    try:
        colour_name = name_color(sys.argv[1])
        print(colour_name)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
