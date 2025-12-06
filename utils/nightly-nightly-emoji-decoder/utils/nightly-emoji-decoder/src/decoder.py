"""emoji_decoder

A tiny module that translates emojis to words using a static dictionary.

Public API
----------
- `decode(emojis: str) -> str`
    Convert a string of emojis into a space‑separated phrase.
- CLI entry point
    `python -m src.decoder "<emoji string>"`
"""

from __future__ import annotations

import sys
from typing import Dict

# Internal mapping of emojis to words.
# Extend this dictionary to support more emojis.
_EMOJI_MAP: Dict[str, str] = {
    "🚀": "rocket",
    "🌕": "moon",
    "🧩": "puzzle",
    "🔧": "wrench",
    "🐍": "snake",
    "📚": "books",
    "☕": "coffee",
    "💡": "idea",
    "🎉": "party",
    "❤️": "love",
}

def decode(emojis: str) -> str:
    """Translate a sequence of emojis into a space‑separated phrase.

    Unknown emojis are represented by the placeholder "?".
    """
    words = []
    for char in emojis:
        word = _EMOJI_MAP.get(char, "?")
        words.append(word)
    return " ".join(words)

def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.decoder \"<emoji string>\"")
        sys.exit(1)
    input_emojis = sys.argv[1]
    print(decode(input_emojis))

if __name__ == "__main__":
    _cli()
