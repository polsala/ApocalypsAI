"""leetify.py – Convert text to leet (1337) speak.

Provides:
- `leetify(text: str) -> str` – core transformation.
- CLI entry‑point when executed as a module.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict

# Mapping based on common leet conventions.
_LEET_MAP: Dict[str, str] = {
    "a": "4",
    "b": "8",
    "c": "(",
    "d": "|)",
    "e": "3",
    "f": "ph",
    "g": "6",
    "h": "#",
    "i": "1",
    "j": "_|",
    "k": "|<",
    "l": "1",
    "m": "/\\/\\",
    "n": "|\\|",
    "o": "0",
    "p": "|*",
    "q": "(_,)",
    "r": "|2",
    "s": "5",
    "t": "7",
    "u": "(_)",
    "v": "\\/",
    "w": "\\/\\/",
    "x": "><",
    "y": "`/",
    "z": "2",
}


def leetify(text: str) -> str:
    """Return a leet‑speak version of *text*.

    The transformation is case‑insensitive; characters not in the mapping are left unchanged.
    """
    result_chars = []
    for ch in text:
        lower = ch.lower()
        if lower in _LEET_MAP:
            # Preserve original case for letters that have a distinct mapping (e.g., "A" -> "4").
            result_chars.append(_LEET_MAP[lower])
        else:
            result_chars.append(ch)
    return "".join(result_chars)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert text to leet (1337) speak.")
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to leetify. If omitted, reads from STDIN.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    if args.text is not None:
        input_text = args.text
    else:
        # Read entire stdin (supports piped input)
        input_text = sys.stdin.read()
    print(leetify(input_text))


if __name__ == "__main__":
    main()
