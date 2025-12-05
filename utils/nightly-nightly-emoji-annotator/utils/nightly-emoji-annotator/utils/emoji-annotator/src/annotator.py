#!/usr/bin/env python3
"""
emoji_annotator: add emojis to text based on simple keyword mapping.
"""

import sys
import argparse
from typing import Dict

# Simple keyword -> emoji mapping
EMOJI_MAP: Dict[str, str] = {
    "coffee": "☕",
    "tea": "🍵",
    "code": "💻",
    "coding": "💻",
    "python": "🐍",
    "bug": "🐛",
    "fire": "🔥",
    "love": "❤️",
    "star": "⭐",
    "rocket": "🚀",
    "music": "🎵",
    "book": "📚",
}


def annotate(text: str) -> str:
    """Return text with emojis appended after recognized keywords.

    The function splits the input on whitespace, strips common punctuation
    from each token for lookup, and if a keyword is found, appends the emoji
    after the original token (preserving punctuation).
    """
    words = text.split()
    annotated = []
    for w in words:
        key = w.strip('.,!?:;').lower()
        emoji = EMOJI_MAP.get(key)
        if emoji:
            annotated.append(f"{w} {emoji}")
        else:
            annotated.append(w)
    return " ".join(annotated)


def main() -> None:
    parser = argparse.ArgumentParser(description="Annotate text with emojis.")
    parser.add_argument("text", nargs="?", help="Text to annotate. If omitted, reads stdin.")
    args = parser.parse_args()

    if args.text is not None:
        input_text = args.text
    else:
        input_text = sys.stdin.read()

    print(annotate(input_text))


if __name__ == "__main__":
    main()
