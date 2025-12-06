"""mood-emoji-mapper – map a short mood description to an emoji.

The implementation is deliberately lightweight: a static ordered list of
(keyword, emoji) pairs is scanned for the first match.  This makes the
behaviour deterministic and fully offline.

Typical usage::

    from src.mapper import map_mood_to_emoji
    print(map_mood_to_emoji("I feel great!"))  # => "😄"
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Tuple

# Ordered mapping – earlier entries have higher priority.
_MOOD_EMOJI_MAP: List[Tuple[str, str]] = [
    ("happy", "😄"),
    ("joy", "😂"),
    ("laugh", "😆"),
    ("excited", "🚀"),
    ("love", "❤️"),
    ("sad", "😢"),
    ("cry", "😭"),
    ("angry", "😠"),
    ("mad", "🤬"),
    ("tired", "😴"),
    ("sleep", "😴"),
    ("bored", "😐"),
    ("confused", "🤔"),
    ("surprised", "😲"),
    ("fear", "😨"),
    ("scared", "😱"),
    ("meh", "😑"),
]

_DEFAULT_EMOJI = "😐"


def map_mood_to_emoji(text: str) -> str:
    """Return an emoji that best matches the supplied *text*.

    The function normalises *text* to lower‑case and searches for the first
    keyword present in the ordered ``_MOOD_EMOJI_MAP``.  If none match, a
    neutral face is returned.
    """
    lowered = text.lower()
    for keyword, emoji in _MOOD_EMOJI_MAP:
        if keyword in lowered:
            return emoji
    return _DEFAULT_EMOJI


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="mood-emoji-mapper",
        description="Map a short mood description to a single emoji.",
    )
    parser.add_argument("mood", help="Mood description, e.g. \"I am happy\"")
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    emoji = map_mood_to_emoji(args.mood)
    print(emoji)


if __name__ == "__main__":
    # When executed as a script, behave like a tiny CLI.
    main()
