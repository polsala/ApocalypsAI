"""nightly-emoji-mood-logger source module.

Provides a simple function `get_mood_emoji` that maps a piece of text to an emoji
representing the inferred mood using keyword heuristics.
"""

from __future__ import annotations

import argparse
import sys
from typing import List

# Keyword groups for each mood
_MOOD_KEYWORDS = {
    "happy": ["happy", "joy", "joyful", "glad", "delighted", "love", "excited"],
    "sad": ["sad", "sorrow", "grief", "down", "depressed", "unhappy", "melancholy"],
    "angry": ["angry", "mad", "furious", "irate", "annoyed", "upset"],
}

# Corresponding emojis
_MOOD_EMOJIS = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "neutral": "😐",
}


def _detect_mood(text: str) -> str:
    """Return the mood key (happy|sad|angry) based on keyword presence.

    The first matching keyword determines the mood. If none match, returns
    "neutral".
    """
    lowered = text.lower()
    for mood, keywords in _MOOD_KEYWORDS.items():
        for kw in keywords:
            if kw in lowered:
                return mood
    return "neutral"


def get_mood_emoji(text: str) -> str:
    """Public API – map *text* to an emoji.

    Parameters
    ----------
    text: str
        Input string to analyse.

    Returns
    -------
    str
        Emoji representing the inferred mood.
    """
    mood = _detect_mood(text)
    return _MOOD_EMOJIS[mood]


def _cli(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="nightly-emoji-mood-logger",
        description="Infer a mood emoji from a line of text.",
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to analyse. If omitted, reads from STDIN.",
    )
    args = parser.parse_args(argv)

    if args.text is not None:
        input_text = args.text
    else:
        # Read from stdin, strip trailing newlines
        input_text = sys.stdin.read().strip()

    if not input_text:
        parser.error("No input text provided.")
        return 1

    emoji = get_mood_emoji(input_text)
    print(emoji)
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
