#!/usr/bin/env python3
"""
emoji_annotator: add emojis to text based on keyword mapping.
"""

import argparse
import sys
from pathlib import Path

# Static keyword to emoji mapping
KEYWORD_EMOJI_MAP = {
    "love": "❤️",
    "fire": "🔥",
    "star": "⭐",
    "rocket": "🚀",
    "bug": "🐞",
    "success": "✅",
    "warning": "⚠️",
    "error": "❌",
    "question": "❓",
    "idea": "💡",
}


def annotate_text(text: str) -> str:
    """Return text with emojis appended after each keyword occurrence.

    The matching is case‑insensitive and only whole words are considered.
    """
    def replace_word(word: str) -> str:
        lower = word.lower()
        emoji = KEYWORD_EMOJI_MAP.get(lower)
        return f"{word}{emoji}" if emoji else word

    # Split while preserving delimiters (punctuation, whitespace)
    import re
    tokens = re.split(r"(\W+)", text)  # keep delimiters as separate tokens
    annotated = [replace_word(tok) for tok in tokens]
    return "".join(annotated)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Annotate a text file with emojis based on keywords."
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to the input text file."
    )
    args = parser.parse_args(argv)

    if not args.path.is_file():
        sys.exit(f"Error: {args.path} is not a file")

    text = args.path.read_text(encoding="utf-8")
    annotated = annotate_text(text)
    sys.stdout.write(annotated)


if __name__ == "__main__":
    main()
