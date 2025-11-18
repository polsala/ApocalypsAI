"""emoji-annotator – enrich text with emojis.

The module provides a single public function ``annotate`` that walks through the
input string word‑by‑word and appends an emoji when the word is present in the
hard‑coded ``WORD_EMOJI_MAP``.

The implementation is deliberately tiny and has **no external dependencies**.
"""

from __future__ import annotations

import sys
from typing import Dict

# ---------------------------------------------------------------------------
# Simple word‑to‑emoji map (offline, deterministic)
# ---------------------------------------------------------------------------
WORD_EMOJI_MAP: Dict[str, str] = {
    "love": "❤️",
    "pizza": "🍕",
    "happy": "😊",
    "birthday": "🎂",
    "good": "👍",
    "morning": "🌅",
    "world": "🌍",
    "sun": "☀️",
    "cat": "🐱",
    "dog": "🐶",
    "coffee": "☕",
    "code": "💻",
    "debug": "🐞",
    "fire": "🔥",
    "star": "⭐",
}


def get_emoji(word: str) -> str:
    """Return the emoji for *word* if it exists, else an empty string.

    The lookup is case‑insensitive.  This function is isolated so that unit
    tests can monkey‑patch it with deterministic behaviour.
    """
    return WORD_EMOJI_MAP.get(word.lower(), "")


def annotate(text: str) -> str:
    """Annotate *text* by appending emojis after known words.

    Example
    -------
    >>> annotate("I love pizza")
    'I ❤️ love ❤️ pizza 🍕'
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    words = text.split()
    annotated_parts = []
    for word in words:
        emoji = get_emoji(word)
        if emoji:
            annotated_parts.append(f"{word} {emoji}")
        else:
            annotated_parts.append(word)
    return " ".join(annotated_parts)


def _cli() -> None:
    """Simple CLI entry point used when the module is executed as a script.

    Usage:
        python -m utils.emoji-annotator.src.annotator "some text"
    """
    if len(sys.argv) != 2:
        print("Usage: python -m utils.emoji-annotator.src.annotator \"<text>\"")
        sys.exit(1)
    input_text = sys.argv[1]
    print(annotate(input_text))


if __name__ == "__main__":
    _cli()
