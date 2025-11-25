"""emoji_mood_logger

A tiny utility that maps a short mood description to an emoji.

Usage:
    python -m src.logger "I am feeling ecstatic"
"""

import sys
from typing import Dict

# Simple keyword to emoji mapping
MOOD_MAP: Dict[str, str] = {
    "happy": "😄",
    "joy": "😄",
    "glad": "😊",
    "excited": "🤩",
    "ecstatic": "🤩",
    "sad": "😢",
    "down": "😔",
    "depressed": "😞",
    "angry": "😠",
    "mad": "😡",
    "frustrated": "😤",
    "tired": "😫",
    "sleepy": "😴",
    "surprised": "😲",
    "shocked": "😱",
    "confused": "🤔",
    "bored": "😐",
    "neutral": "😐",
}

DEFAULT_EMOJI = "😐"

def mood_to_emoji(text: str) -> str:
    """Return an emoji representing the mood described in *text*.

    The function lower‑cases the input and looks for any keyword from
    ``MOOD_MAP``. The first match wins. If no keyword is found, a neutral
    face is returned.
    """
    lowered = text.lower()
    for keyword, emoji in MOOD_MAP.items():
        if keyword in lowered:
            return emoji
    return DEFAULT_EMOJI

def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: python -m src.logger \"your mood description\"")
        return 2
    description = " ".join(argv)
    print(mood_to_emoji(description))
    return 0

if __name__ == "__main__":
    sys.exit(main())
