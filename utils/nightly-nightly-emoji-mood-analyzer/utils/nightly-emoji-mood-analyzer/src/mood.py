"""emoji_mood_analyzer

A tiny, dependency‑free module that maps short text to an emoji representing its mood.

Public API
----------

- ``analyze_mood(text: str) -> str``: Return an emoji string.

Running as a script prints the emoji for the supplied argument.
"""

from __future__ import annotations

import sys
from typing import Dict, List

# Mapping of keyword groups to emojis. Order matters – first match wins.
_MOOD_MAP: List[tuple[list[str], str]] = [
    ("happy excited joyful thrilled".split(), "😊"),
    ("sad depressed gloomy lonely".split(), "😢"),
    ("angry mad furious irritated".split(), "😠"),
    ("love adore cherish".split(), "❤️"),
    ("fear scared terrified terrified".split(), "😱"),
]

_DEFAULT_EMOJI = "🤔"


def _tokenize(text: str) -> List[str]:
    """Very simple whitespace tokenizer, lower‑casing the input."""
    return text.lower().split()


def analyze_mood(text: str) -> str:
    """Return an emoji that best matches the mood of *text*.

    The function scans the token list for any keyword in ``_MOOD_MAP``.
    The first matching group determines the emoji. If no match is found,
    ``_DEFAULT_EMOJI`` is returned.
    """
    tokens = set(_tokenize(text))
    for keywords, emoji in _MOOD_MAP:
        if any(word in tokens for word in keywords):
            return emoji
    return _DEFAULT_EMOJI


def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m utils.nightly-emoji-mood-analyzer.src.mood \"<text>\"")
        sys.exit(1)
    text = sys.argv[1]
    print(analyze_mood(text))


if __name__ == "__main__":
    _cli()
