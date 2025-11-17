"""Emoji Mood Tracker utility."""

import sys
from typing import List

POSITIVE_WORDS: List[str] = [
    "love",
    "great",
    "awesome",
    "fantastic",
    "good",
    "happy",
    "joy",
    "excellent",
    "wonderful",
    "delight",
]

NEGATIVE_WORDS: List[str] = [
    "hate",
    "bad",
    "terrible",
    "sad",
    "angry",
    "awful",
    "worst",
    "pain",
    "depress",
    "disappoint",
]


def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the overall mood of *text*.

    Simple heuristic: count occurrences of positive and negative keywords.
    If positives > negatives → 😊, if negatives > positives → ☹️, else 😐.
    """
    lowered = text.lower()
    pos = sum(word in lowered for word in POSITIVE_WORDS)
    neg = sum(word in lowered for word in NEGATIVE_WORDS)

    if pos > neg:
        return "😊"
    if neg > pos:
        return "☹️"
    return "😐"


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) != 2:
        print("Usage: python -m emoji_mood \"Your text here\"")
        sys.exit(1)
    print(get_mood_emoji(sys.argv[1]))


if __name__ == "__main__":
    main()
