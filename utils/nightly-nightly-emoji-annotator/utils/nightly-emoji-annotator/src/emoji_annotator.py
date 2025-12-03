#!/usr/bin/env python3
"""
Emoji Annotator utility.

Provides a function `annotate(text: str) -> str` that inserts emojis
after known keywords. Also offers a CLI entry point.
"""

import sys
from typing import Dict

# Static keyword -> emoji mapping
EMOJI_MAP: Dict[str, str] = {
    "coffee": "☕",
    "tea": "🍵",
    "code": "💻",
    "coding": "💻",
    "python": "🐍",
    "love": "❤️",
    "fire": "🔥",
    "star": "⭐",
    "music": "🎵",
    "book": "📚",
}


def annotate(text: str) -> str:
    """Return text with emojis appended after known keywords.

    The function preserves original punctuation and whitespace.
    """
    words = text.split()
    result = []
    for word in words:
        # Strip surrounding punctuation for matching
        stripped = word.strip('.,!?:;')
        emoji = EMOJI_MAP.get(stripped.lower())
        if emoji:
            # Preserve any trailing punctuation that was stripped
            suffix = word[len(stripped):]
            result.append(f"{stripped}{emoji}{suffix}")
        else:
            result.append(word)
    return " ".join(result)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: emoji_annotator.py <text>", file=sys.stderr)
        sys.exit(1)
    input_text = " ".join(argv)
    print(annotate(input_text))


if __name__ == "__main__":
    main()
