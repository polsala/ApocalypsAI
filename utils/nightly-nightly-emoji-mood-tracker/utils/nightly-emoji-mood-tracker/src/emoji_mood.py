"""emoji_mood.py

A tiny sentiment‑to‑emoji mapper.

Public API:
    get_mood_emoji(text: str) -> str
        Returns an emoji representing the mood of *text*.

CLI usage:
    python -m src.emoji_mood "Your text here"
    echo "Your text" | python -m src.emoji_mood
"""

from __future__ import annotations
import sys
from collections import Counter
from typing import Dict, List

# Keyword groups for each mood – deterministic and offline.
MOOD_KEYWORDS: Dict[str, List[str]] = {
    "happy": ["happy", "joy", "joyful", "glad", "great", "fantastic", "awesome", "delighted", "pleased", "cheerful"],
    "sad": ["sad", "down", "depressed", "unhappy", "blue", "gloomy", "miserable", "tearful", "heartbroken"],
    "angry": ["angry", "mad", "furious", "irate", "annoyed", "upset", "livid", "resentful"],
}

EMOJI_MAP: Dict[str, str] = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "neutral": "😐",
}

def _tokenise(text: str) -> List[str]:
    """Very simple whitespace/token punctuation tokeniser.
    Returns lower‑cased words without surrounding punctuation.
    """
    import re
    # Split on non‑word characters, filter empty strings.
    return [t.lower() for t in re.split(r"\W+", text) if t]

def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the sentiment of *text*.

    The algorithm counts how many keywords from each mood appear in the
    tokenised input. The mood with the highest count wins. Ties or zero matches
    default to ``neutral``.
    """
    tokens = _tokenise(text)
    counter = Counter()
    for mood, keywords in MOOD_KEYWORDS.items():
        matches = sum(tok in keywords for tok in tokens)
        counter[mood] = matches
    # Determine the mood with the highest count.
    most_common = counter.most_common()
    if not most_common:
        return EMOJI_MAP["neutral"]
    top_mood, top_count = most_common[0]
    # Check for tie with second place.
    if len(most_common) > 1 and top_count == most_common[1][1]:
        return EMOJI_MAP["neutral"]
    if top_count == 0:
        return EMOJI_MAP["neutral"]
    return EMOJI_MAP.get(top_mood, EMOJI_MAP["neutral"])

def _cli() -> None:
    """Entry‑point for ``python -m src.emoji_mood``.
    Reads from the first CLI argument if present, otherwise from STDIN.
    """
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
    else:
        input_text = sys.stdin.read().strip()
    emoji = get_mood_emoji(input_text)
    print(emoji)

if __name__ == "__main__":
    _cli()
