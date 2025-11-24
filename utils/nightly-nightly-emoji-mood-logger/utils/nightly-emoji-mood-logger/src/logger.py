"""emoji_mood_logger – map short text to a mood emoji.

This module provides a single public function :func:`get_mood_emoji` and a tiny
CLI wrapper so the utility can be invoked via ``python -m src.logger "text"``.
"""

from __future__ import annotations

import argparse
import sys
from typing import List

# Simple keyword‑to‑emoji mapping. Order matters – first match wins.
_MOOD_MAP: List[tuple[list[str], str]] = [
    (['happy', 'joy', 'delighted', 'great'], "😊"),
    (['sad', 'sorrow', 'down', 'upset'], "😢"),
    (['angry', 'mad', 'furious', 'hate'], "😠"),
    (['love', 'adore', 'cherish'], "❤️"),
    (['surprise', 'wow', 'amazed'], "😲"),
]

_DEFAULT_EMOJI = "🤔"


def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The function performs a case‑insensitive search for any of the keywords
    defined in ``_MOOD_MAP``. The first matching group determines the emoji.
    If no keywords are found, ``_DEFAULT_EMOJI`` is returned.

    Parameters
    ----------
    text:
        Input string describing a feeling or situation.

    Returns
    -------
    str
        A single Unicode emoji.
    """
    lowered = text.lower()
    for keywords, emoji in _MOOD_MAP:
        if any(keyword in lowered for keyword in keywords):
            return emoji
    return _DEFAULT_EMOJI


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="emoji-mood-logger",
        description="Map a short text snippet to a mood emoji.",
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to analyse. If omitted, reads from STDIN.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    if args.text is not None:
        input_text = args.text
    else:
        # Read from stdin when no positional argument is supplied.
        input_text = sys.stdin.read().strip()
    emoji = get_mood_emoji(input_text)
    print(emoji)


if __name__ == "__main__":
    main()
