"""
emoji_mood_analyzer

Provides a simple function to map text to a mood emoji based on keyword heuristics.
"""

import sys
from typing import Dict

# Mapping of lower‑case keyword to emoji.
KEYWORD_EMOJI_MAP: Dict[str, str] = {
    "love": "😄",
    "happy": "😊",
    "joy": "😂",
    "excited": "🤩",
    "great": "👍",
    "good": "🙂",
    "awesome": "🤗",
    "sad": "😢",
    "bad": "🙁",
    "angry": "😠",
    "hate": "🤬",
    "tired": "😴",
    "bored": "😐",
    "confused": "🤔",
    "surprised": "😲",
    "fear": "😨",
    "scared": "😱",
}

DEFAULT_EMOJI = "😐"


def analyze_mood(text: str) -> str:
    """
    Return an emoji representing the mood of the given text.

    The function lower‑cases the text and returns the emoji for the first
    keyword found in ``KEYWORD_EMOJI_MAP``. If no keyword matches, ``DEFAULT_EMOJI`` is returned.
    """
    lowered = text.lower()
    for keyword, emoji in KEYWORD_EMOJI_MAP.items():
        if keyword in lowered:
            return emoji
    return DEFAULT_EMOJI


def main(argv: list[str] | None = None) -> int:
    """
    CLI entry point.

    Usage:
        python -m emoji_mood_analyzer "your text here"
    """
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("Usage: python -m emoji_mood_analyzer \"your text here\"")
        return 2

    text = " ".join(argv)
    emoji = analyze_mood(text)
    print(emoji)
    return 0


if __name__ == "__main__":
    sys.exit(main())
