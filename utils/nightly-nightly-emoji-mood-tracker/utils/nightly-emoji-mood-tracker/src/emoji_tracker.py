"""emoji_tracker.py

A tiny, dependency‑free utility that returns a mood emoji for a given text.

The heuristic is deliberately simple and deterministic:
- If any *happy* keywords are present → 😊
- If any *sad* keywords are present → 😢
- If any *angry* keywords are present → 😠
- Otherwise → 🤔

The module can be used programmatically via `get_mood_emoji(text)` or from the command line.
"""

from __future__ import annotations

import argparse
import sys
from typing import List

# Keyword groups – kept small for deterministic behaviour
_HAPPY_KEYWORDS: List[str] = ["happy", "joy", "love", "great", "awesome", "fantastic", "good", "wonderful"]
_SAD_KEYWORDS: List[str] = ["sad", "unhappy", "bad", "terrible", "depressed", "down", "sorrow"]
_ANGRY_KEYWORDS: List[str] = ["angry", "mad", "furious", "irate", "annoyed", "upset"]

_EMOJI_MAP = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "neutral": "🤔",
}

def _contains_keyword(text: str, keywords: List[str]) -> bool:
    """Return True if any keyword appears in *text* (case‑insensitive)."""
    lowered = text.lower()
    return any(word in lowered for word in keywords)

def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the overall mood of *text*.

    The function checks the keyword groups in order of precedence:
    happy → sad → angry → neutral.
    """
    if _contains_keyword(text, _HAPPY_KEYWORDS):
        return _EMOJI_MAP["happy"]
    if _contains_keyword(text, _SAD_KEYWORDS):
        return _EMOJI_MAP["sad"]
    if _contains_keyword(text, _ANGRY_KEYWORDS):
        return _EMOJI_MAP["angry"]
    return _EMOJI_MAP["neutral"]

def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Return a mood emoji for a given text.")
    parser.add_argument("text", nargs="?", help="Text to analyse. If omitted, reads from stdin.")
    return parser.parse_args(argv)

def main() -> None:
    args = _parse_args()
    if args.text:
        text = args.text
    else:
        # Read from stdin when no argument is supplied
        text = sys.stdin.read()
    emoji = get_mood_emoji(text)
    print(emoji)

if __name__ == "__main__":
    main()
