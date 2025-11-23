"""emoji_mood.py

Utility to map a short piece of text to a mood‑representing emoji.

The implementation is deliberately lightweight: it scans the text for
pre‑defined keyword groups and returns the first matching emoji. If no
keywords are found, a neutral emoji is returned.

The module can be executed as a script for quick ad‑hoc usage.
"""

from __future__ import annotations

import argparse
import re
from typing import List

# Keyword groups – order matters (first match wins)
MOOD_KEYWORDS = {
    "happy": ["happy", "joy", "fantastic", "great", "awesome", "glad", "delighted", "pleased"],
    "sad": ["sad", "down", "unhappy", "depressed", "blue", "melancholy", "gloomy"],
    "angry": ["angry", "mad", "furious", "irate", "annoyed", "upset"],
}

MOOD_EMOJIS = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "neutral": "😐",
}

def _normalize(text: str) -> str:
    """Lower‑case and strip punctuation for simple matching."""
    return re.sub(r"[\W_]+", " ", text.lower()).strip()

def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The function performs a case‑insensitive search for any of the keywords
    defined in ``MOOD_KEYWORDS``. The first matching mood category determines
    the emoji. If no keywords are found, a neutral emoji is returned.
    """
    normalized = _normalize(text)
    words: List[str] = normalized.split()
    for mood, keywords in MOOD_KEYWORDS.items():
        if any(keyword in words for keyword in keywords):
            return MOOD_EMOJIS[mood]
    return MOOD_EMOJIS["neutral"]

def _cli() -> None:
    parser = argparse.ArgumentParser(description="Return a mood emoji for a given text.")
    parser.add_argument("text", help="The text to analyse")
    args = parser.parse_args()
    emoji = get_mood_emoji(args.text)
    print(emoji)

if __name__ == "__main__":
    _cli()
