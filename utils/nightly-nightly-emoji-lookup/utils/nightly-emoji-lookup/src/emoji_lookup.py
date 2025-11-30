"""emoji_lookup.py

A tiny lookup table for emoji → CLDR short name.

Provides:
- ``EMOJI_MAP`` – static dictionary of a handful of emojis.
- ``get_name`` – return the short name or ``None`` if unknown.
- CLI entry‑point when executed as a module.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, Optional

# Mock rationale: a small, deterministic subset of the full CLDR emoji list.
EMOJI_MAP: Dict[str, str] = {
    "😀": "grinning face",
    "🚀": "rocket",
    "❤️": "red heart",
    "👍": "thumbs up",
    "🐍": "snake",
    "🌟": "glowing star",
}


def get_name(emoji: str) -> Optional[str]:
    """Return the CLDR short name for *emoji*.

    If the emoji is not present in ``EMOJI_MAP`` the function returns ``None``.
    """
    return EMOJI_MAP.get(emoji)


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Lookup CLDR short name for an emoji.")
    parser.add_argument("emoji", help="The emoji character to look up.")
    args = parser.parse_args()

    name = get_name(args.emoji)
    if name:
        print(name)
    else:
        print("Unknown emoji", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
