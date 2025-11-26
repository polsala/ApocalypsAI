#!/usr/bin/env python3
"""
Emoji Mood Analyzer

Scans text for simple sentiment keywords and reports an emoji histogram.
"""

import argparse
import sys
from collections import Counter
from typing import Dict, List

# Keyword lists (simple, offline)
HAPPY_WORDS = {"happy", "joy", "glad", "delight", "pleased", "cheerful", "smile"}
SAD_WORDS = {"sad", "unhappy", "sorrow", "down", "depressed", "gloom", "tear"}
ANGRY_WORDS = {"angry", "mad", "furious", "irate", "annoyed", "rage", "outraged"}
NEUTRAL_WORDS = {"okay", "fine", "average", "normal", "so-so", "meh"}

EMOJI_MAP = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "neutral": "😐",
}

def _tokenize(text: str) -> List[str]:
    """Very simple tokenizer: lower‑case and split on non‑alphabetic characters."""
    import re
    return re.findall(r"[a-z]+", text.lower())

def analyze_mood(text: str) -> Dict[str, int]:
    """Return a dict mapping emoji to count based on keyword occurrences."""
    tokens = _tokenize(text)
    counter = Counter(tokens)

    counts = {
        EMOJI_MAP["happy"]: sum(counter[w] for w in HAPPY_WORDS),
        EMOJI_MAP["sad"]: sum(counter[w] for w in SAD_WORDS),
        EMOJI_MAP["angry"]: sum(counter[w] for w in ANGRY_WORDS),
        EMOJI_MAP["neutral"]: sum(counter[w] for w in NEUTRAL_WORDS),
    }
    return counts

def _print_counts(counts: Dict[str, int]) -> None:
    for emoji, cnt in sorted(counts.items(), key=lambda kv: kv[0]):
        print(f"{emoji}: {cnt}")

def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Emoji Mood Analyzer")
    parser.add_argument("path", help="Path to a UTF‑8 text file")
    args = parser.parse_args(argv)

    try:
        with open(args.path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"File not found: {args.path}", file=sys.stderr)
        return 1

    counts = analyze_mood(text)
    _print_counts(counts)
    return 0

if __name__ == "__main__":
    sys.exit(main())
