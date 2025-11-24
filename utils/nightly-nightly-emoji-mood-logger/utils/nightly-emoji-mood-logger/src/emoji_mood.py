"""emoji_mood.py

Utility to translate plain‑text sentences into emoji‑rich strings.

The module provides:
- `EMOJI_MAP`: a static dictionary mapping lower‑case words/phrases to emojis.
- `translate(text: str) -> str`: returns the transformed string.
- A simple CLI entry‑point when executed as a module.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict

# ---------------------------------------------------------------------------
# Static emoji mapping – deterministic and offline.
# ---------------------------------------------------------------------------
EMOJI_MAP: Dict[str, str] = {
    "love": "❤️",
    "happy": "😊",
    "sad": "😢",
    "excited": "🤩",
    "angry": "😠",
    "laugh": "😂",
    "code": "💻",
    "coding": "💻",
    "python": "🐍",
    "coffee": "☕",
    "tea": "🍵",
    "sun": "☀️",
    "moon": "🌙",
    "star": "⭐",
    "fire": "🔥",
    "water": "💧",
    "earth": "🌍",
    "music": "🎵",
    "book": "📚",
    "dog": "🐶",
    "cat": "🐱",
    "pizza": "🍕",
    "cake": "🍰",
    "party": "🥳",
    "thanks": "🙏",
    "welcome": "🤗",
    # Add more as needed.
}


def _tokenize(text: str) -> list[str]:
    """Very simple whitespace tokenizer preserving punctuation.

    This is sufficient for the demo and keeps the utility lightweight.
    """
    return text.split()


def translate(text: str) -> str:
    """Translate *text* by replacing known words with their emoji equivalents.

    The replacement is case‑insensitive and only whole‑word matches are
    considered. Punctuation attached to a word is preserved.
    """
    if not isinstance(text, str):
        raise TypeError("translate expects a string")

    tokens = _tokenize(text)
    result_tokens: list[str] = []
    for token in tokens:
        # Strip surrounding punctuation for lookup, keep it to re‑attach.
        stripped = token.strip(".,!?:;\"'()[]{}")
        lower = stripped.lower()
        emoji = EMOJI_MAP.get(lower)
        if emoji:
            # Preserve original punctuation.
            prefix = token[: token.find(stripped)] if token.find(stripped) != -1 else ""
            suffix = token[token.find(stripped) + len(stripped) :] if token.find(stripped) != -1 else ""
            result_tokens.append(f"{prefix}{emoji}{suffix}")
        else:
            result_tokens.append(token)
    return " ".join(result_tokens)


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Translate a sentence into an emoji‑rich version."
    )
    parser.add_argument("text", nargs="+", help="Text to translate (will be joined with spaces)")
    args = parser.parse_args()
    input_text = " ".join(args.text)
    print(translate(input_text))


if __name__ == "__main__":
    # When executed as a module: python -m utils.nightly-emoji-mood-logger.src.emoji_mood "..."
    _cli()
