"""mood_meter.py

Provides a simple function to map a short piece of text to a mood emoji.

The implementation is deliberately lightweight – no external dependencies –
so the utility can run in the minimal Python environment used by the CI.
"""

from __future__ import annotations

import sys
from typing import Set

# Keyword sets – all lower‑case for case‑insensitive matching
_POSITIVE_WORDS: Set[str] = {
    "good",
    "great",
    "fixed",
    "awesome",
    "success",
    "happy",
    "love",
    "nice",
    "excellent",
}

_NEGATIVE_WORDS: Set[str] = {
    "bad",
    "fail",
    "error",
    "bug",
    "sad",
    "unhappy",
    "hate",
    "poor",
}

_ANGRY_WORDS: Set[str] = {
    "angry",
    "mad",
    "furious",
    "rage",
    "irate",
}

# Emoji constants
_ANGRY_EMOJI = "😡"
_POSITIVE_EMOJI = "😊"
_NEGATIVE_EMOJI = "😞"
_DEFAULT_EMOJI = "🤔"


def _tokenize(text: str) -> Set[str]:
    """Return a set of lower‑case words extracted from *text*.

    Simple whitespace split plus stripping of punctuation. This is sufficient
    for the deterministic tests and keeps the implementation tiny.
    """
    import string

    translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
    cleaned = text.translate(translator).lower()
    return set(cleaned.split())


def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the *mood* of *text*.

    Priority order:
    1. Angry words → 😡
    2. Positive words → 😊
    3. Negative words → 😞
    4. Fallback → 🤔
    """
    tokens = _tokenize(text)

    if tokens & _ANGRY_WORDS:
        return _ANGRY_EMOJI
    if tokens & _POSITIVE_WORDS:
        return _POSITIVE_EMOJI
    if tokens & _NEGATIVE_WORDS:
        return _NEGATIVE_EMOJI
    return _DEFAULT_EMOJI


def _cli() -> None:
    """Simple command‑line interface.

    Usage: ``python -m nightly_emoji_mood_meter "some text"``
    """
    if len(sys.argv) < 2:
        print("Usage: python -m nightly_emoji_mood_meter \"your text\"")
        sys.exit(2)
    input_text = " ".join(sys.argv[1:])
    print(get_mood_emoji(input_text))


if __name__ == "__main__":
    _cli()
