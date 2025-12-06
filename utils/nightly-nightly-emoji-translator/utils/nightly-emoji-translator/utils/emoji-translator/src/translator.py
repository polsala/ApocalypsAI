#!/usr/bin/env python3
"""
emoji-translator utility

Provides a simple function `translate` that replaces predefined keywords with emojis.
Can be used as a CLI: `python src/translator.py "I love cats"` prints the translated text.
"""

import sys
import re
from typing import Dict

# Mapping of lowercase words to their emoji representations
EMOJI_MAP: Dict[str, str] = {
    "love": "❤️",
    "star": "⭐",
    "fire": "🔥",
    "smile": "😊",
    "cat": "🐱",
    "dog": "🐶",
    "pizza": "🍕",
    "coffee": "☕",
    "sun": "☀️",
    "moon": "🌙",
}

# Compile a regex that matches any of the keys as whole words, case‑insensitive
WORD_RE = re.compile(
    r"\b({})\b".format("|".join(map(re.escape, EMOJI_MAP.keys()))),
    flags=re.IGNORECASE,
)


def _replace(match: re.Match) -> str:
    """Return the emoji for the matched word, preserving original case handling via lower‑casing."""
    word = match.group(0).lower()
    return EMOJI_MAP.get(word, word)


def translate(text: str) -> str:
    """Replace all occurrences of known keywords in *text* with their emojis.

    The replacement is deterministic and respects word boundaries.
    """
    return WORD_RE.sub(_replace, text)


def _cli() -> None:
    """Simple command‑line interface.

    - If arguments are supplied, they are joined into a single string.
    - Otherwise, the script reads from STDIN.
    The translated result is printed to STDOUT.
    """
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
    else:
        input_text = sys.stdin.read()
    print(translate(input_text))


if __name__ == "__main__":
    _cli()
