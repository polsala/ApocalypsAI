"""emoji_lookup
================
A tiny emoji lookup library.

Provides:
- ``get_emoji(name)`` – return the Unicode character for a short name.
- ``get_name(char)`` – return the short name for a Unicode character.
- ``main()`` – simple CLI for interactive use.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, Optional

# A modest built‑in emoji dictionary – enough for demo purposes.
EMOJI_MAP: Dict[str, str] = {
    "grinning": "😀",
    "smile": "😄",
    "laugh": "😂",
    "wink": "😉",
    "heart": "❤️",
    "thumbsup": "👍",
    "rocket": "🚀",
    "fire": "🔥",
    "star": "⭐",
    "poop": "💩",
}

# Reverse lookup generated once for efficiency.
_REVERSE_MAP: Dict[str, str] = {v: k for k, v in EMOJI_MAP.items()}


def get_emoji(name: str) -> Optional[str]:
    """Return the Unicode emoji for *name* (case‑insensitive).

    Args:
        name: Short name like ``"rocket"``.
    Returns:
        The emoji character or ``None`` if not found.
    """
    return EMOJI_MAP.get(name.lower())


def get_name(char: str) -> Optional[str]:
    """Return the short name for a Unicode *char*.

    Args:
        char: A single emoji character.
    Returns:
        The short name or ``None`` if unknown.
    """
    return _REVERSE_MAP.get(char)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lookup emojis by name or character.")
    parser.add_argument(
        "query",
        help="Either an emoji short name (e.g., 'rocket') or a single emoji character.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    query = args.query.strip()
    # Heuristic: if the query is a single character and exists in reverse map, treat as char.
    if len(query) == 1 and query in _REVERSE_MAP:
        name = get_name(query)
        print(name)
    else:
        emoji = get_emoji(query)
        if emoji:
            print(emoji)
        else:
            # Fallback: maybe the user supplied an unknown char.
            print(f"No emoji found for '{query}'.", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
