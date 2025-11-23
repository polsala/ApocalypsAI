"""Emoji Mood Tracker utility.

Provides `detect_mood` function and a simple CLI.
"""

import sys
from pathlib import Path
from typing import List

POSITIVE_WORDS = {
    "love",
    "happy",
    "joy",
    "awesome",
    "good",
    "great",
    "fantastic",
    "wonderful",
    "excellent",
    "sunny",
    "bright",
    "pleased",
    "delight",
    "smile",
    "laugh",
}

NEGATIVE_WORDS = {
    "hate",
    "sad",
    "bad",
    "terrible",
    "awful",
    "depressed",
    "gloomy",
    "rainy",
    "angry",
    "upset",
    "pain",
    "sorrow",
    "cry",
    "unhappy",
    "miserable",
}

EMOJI_POSITIVE = "😊"
EMOJI_NEGATIVE = "😢"
EMOJI_NEUTRAL = "😐"


def _tokenize(text: str) -> List[str]:
    """Very simple tokenizer: lower‑case and split on non‑alphabetic characters."""
    import re

    return re.findall(r"[a-z]+", text.lower())


def detect_mood(text: str) -> str:
    """Return an emoji representing the overall mood of *text*."""
    tokens = _tokenize(text)
    pos = sum(token in POSITIVE_WORDS for token in tokens)
    neg = sum(token in NEGATIVE_WORDS for token in tokens)

    if pos > neg:
        return EMOJI_POSITIVE
    if neg > pos:
        return EMOJI_NEGATIVE
    return EMOJI_NEUTRAL


def _read_input(arg: str) -> str:
    """Read text from a file path or treat the argument as raw text."""
    path = Path(arg)
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return arg


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) != 2:
        print("Usage: python -m utils.nightly_emoji_mood_tracker.src.emoji_tracker <text-or-file>")
        sys.exit(1)

    input_text = _read_input(sys.argv[1])
    print(detect_mood(input_text))


if __name__ == "__main__":
    main()
