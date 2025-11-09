#!/usr/bin/env python3
"""
emoji-mood-analyzer

Detects a simple mood from a short text and returns an emoji.

The implementation is deliberately lightweight: it looks for the first
keyword that appears in a predefined mapping and returns the associated
emoji. If no keyword matches, a neutral face (😐) is returned.
"""

import sys
import re
from typing import List

# ---------------------------------------------------------------------------
# Simple keyword → emoji mapping. The order of insertion does not matter –
# the *first* matching word in the input wins.
# ---------------------------------------------------------------------------
MOOD_MAP = {
    "happy": "😊",
    "joy": "😊",
    "glad": "😊",
    "sad": "😢",
    "unhappy": "😢",
    "down": "😢",
    "angry": "😠",
    "mad": "😠",
    "furious": "😠",
    "excited": "🤩",
    "thrilled": "🤩",
    "love": "❤️",
    "loving": "❤️",
    "fear": "😨",
    "scared": "😨",
    "surprised": "😲",
    "confused": "🤔",
    "bored": "😐",
}


def _normalize(text: str) -> List[str]:
    """Return a list of lower‑cased words stripped of punctuation.

    The regular expression extracts word characters (letters, digits, underscore)
    and discards everything else, ensuring deterministic tokenisation.
    """
    return re.findall(r"\b\w+\b", text.lower())


def analyze_mood(text: str) -> str:
    """Return an emoji representing the mood detected in *text*.

    The function scans the words in order; the first word that appears in
    ``MOOD_MAP`` determines the result. If no word matches, a neutral face is
    returned.
    """
    for word in _normalize(text):
        if word in MOOD_MAP:
            return MOOD_MAP[word]
    return "😐"  # neutral face


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Usage example:
        python -m utils.emoji-mood-analyzer.src.mood "I am thrilled!"
    """
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Error: no input text provided.", file=sys.stderr)
        return 1
    text = " ".join(argv)
    print(analyze_mood(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
