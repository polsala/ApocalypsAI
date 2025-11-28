"""emoji_mood.py

Simple keyword‑based mood detector.

Provides:
- `get_mood_emoji(text: str) -> str`
- CLI entry point for quick use.
"""

from __future__ import annotations
import argparse
import sys
from typing import List

_HAPPY_KEYWORDS: List[str] = [
    "happy",
    "joy",
    "love",
    "awesome",
    "great",
    "fantastic",
    "good",
    "wonderful",
    "excited",
    "sunshine",
]

_SAD_KEYWORDS: List[str] = [
    "sad",
    "bad",
    "terrible",
    "depressed",
    "unhappy",
    "angry",
    "pain",
    "hate",
    "miserable",
    "rain",
]

def _contains_keyword(text: str, keywords: List[str]) -> bool:
    """Return True if any keyword appears in *text* (case‑insensitive)."""
    lowered = text.lower()
    return any(word in lowered for word in keywords)

def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    - 😄 if a happy keyword is present.
    - 😢 if a sad keyword is present.
    - 😐 otherwise.
    """
    if _contains_keyword(text, _HAPPY_KEYWORDS):
        return "😄"
    if _contains_keyword(text, _SAD_KEYWORDS):
        return "😢"
    return "😐"

def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect mood emoji from a text snippet.")
    parser.add_argument("text", nargs="?", help="Text to analyze. If omitted, reads from stdin.")
    return parser.parse_args(argv)

def main(argv: List[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.text:
        text = args.text
    else:
        # Read from stdin when no positional argument is given
        text = sys.stdin.read()
    emoji = get_mood_emoji(text)
    print(emoji)
    return 0

if __name__ == "__main__":
    sys.exit(main())
