"""
Emoji Mood Logger utility.

Provides `analyze_mood(text: str) -> str` which returns an emoji representing
the overall sentiment of the given text.
"""

import argparse
import sys
from collections import Counter
from typing import List

# Simple sentiment word lists
POSITIVE_WORDS: List[str] = [
    "happy", "joy", "joyful", "glad", "delight", "delighted", "wonderful",
    "great", "good", "fantastic", "excellent", "love", "lovely", "awesome",
    "pleased", "smile", "smiling", "cheerful", "content", "peace", "peaceful"
]

NEGATIVE_WORDS: List[str] = [
    "sad", "sadness", "unhappy", "depressed", "bad", "terrible", "awful",
    "hate", "hated", "angry", "anger", "pain", "painful", "sick", "sickly",
    "worried", "anxious", "fear", "fearful", "stress", "stressful", "cry"
]

def _tokenize(text: str) -> List[str]:
    """Very naive tokenizer: lower‑case and split on non‑alphabetic characters."""
    import re
    return re.findall(r"[a-z]+", text.lower())


def analyze_mood(text: str) -> str:
    """
    Analyze the sentiment of *text* and return an emoji.

    Returns:
        str: One of "😊", "😢", or "😐".
    """
    tokens = _tokenize(text)
    counts = Counter(tokens)

    pos_score = sum(counts[word] for word in POSITIVE_WORDS)
    neg_score = sum(counts[word] for word in NEGATIVE_WORDS)

    if pos_score > neg_score:
        return "😊"
    elif neg_score > pos_score:
        return "😢"
    else:
        return "😐"


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Return an emoji summarizing the mood of a text file."
    )
    parser.add_argument(
        "path",
        type=str,
        help="Path to a plain‑text file containing the journal entry."
    )
    args = parser.parse_args()

    try:
        with open(args.path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as exc:
        print(f"Error reading file: {exc}", file=sys.stderr)
        sys.exit(1)

    emoji = analyze_mood(content)
    print(emoji)

if __name__ == "__main__":
    _cli()
