"""mood_caster.py

Utility to infer a mood emoji from a short text string.

The implementation is deliberately lightweight – it uses a static
keyword‑to‑emoji map and simple case‑insensitive matching. No external
services are called, making the utility safe for offline execution and
easy to test.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, List

# Simple heuristic mapping. Keys are lower‑case words; values are emojis.
_MOOD_MAP: Dict[str, str] = {
    "happy": "😊",
    "joy": "😊",
    "glad": "😊",
    "delighted": "😊",
    "sad": "😢",
    "unhappy": "😢",
    "down": "😢",
    "depressed": "😢",
    "angry": "😠",
    "mad": "😠",
    "furious": "😠",
    "love": "❤️",
    "loved": "❤️",
    "affection": "❤️",
    "surprised": "😲",
    "shocked": "😲",
    "wow": "😲",
}

_DEFAULT_EMOJI = "🤔"


def _tokenize(text: str) -> List[str]:
    """Return a list of lower‑case words stripped of punctuation.

    This helper is kept separate for easier unit‑testing and potential
    future enhancements (e.g., stemming).
    """
    # Mock rationale: we avoid importing `re` to keep the utility minimal.
    # Simple split on whitespace and strip common punctuation.
    tokens = []
    for word in text.split():
        cleaned = word.strip(".,!?:;\"'()[]{}")
        tokens.append(cleaned.lower())
    return tokens


def get_mood_emoji(text: str) -> str:
    """Return an emoji that best matches the mood of *text*.

    The function scans the tokenised text for any keyword present in
    ``_MOOD_MAP``. The first match wins. If no keywords are found, a
    neutral ``_DEFAULT_EMOJI`` is returned.
    """
    for token in _tokenize(text):
        if token in _MOOD_MAP:
            return _MOOD_MAP[token]
    return _DEFAULT_EMOJI


def _parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Infer a mood emoji from text.")
    parser.add_argument("text", nargs="+", help="Text to analyse (will be joined with spaces)")
    return parser.parse_args()


def main() -> None:
    args = _parse_cli()
    text = " ".join(args.text)
    emoji = get_mood_emoji(text)
    print(emoji)


if __name__ == "__main__":
    # When executed as a module (`python -m src.mood_caster "..."`)
    main()
