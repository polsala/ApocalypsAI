"""emoji_tracker.py

Simple keyword‑based mood‑to‑emoji mapper.

Provides:
* `get_mood_emoji(text: str) -> str` – core function.
* CLI entry point for quick ad‑hoc usage.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from typing import Dict, List

# ---------------------------------------------------------------------------
# Keyword groups → emoji mapping
# ---------------------------------------------------------------------------
MOOD_MAP: Dict[str, List[str]] = {
    "happy": ["happy", "joy", "joyful", "glad", "cheerful", "delighted", "elated", "great", "good", "fantastic", "awesome"],
    "sad": ["sad", "down", "depressed", "unhappy", "blue", "melancholy", "gloomy"],
    "angry": ["angry", "mad", "furious", "irate", "annoyed", "upset"],
    "love": ["love", "loving", "adore", "cherish", "fond", "heart"],
    "fear": ["fear", "scared", "terrified", "afraid", "frightened", "panic"],
}

EMOJI_MAP: Dict[str, str] = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "love": "❤️",
    "fear": "😱",
    "neutral": "😐",
}


def _tokenize(text: str) -> List[str]:
    """Very simple tokenizer: lower‑case and split on whitespace.

    # Mock rationale: we avoid external libs like nltk to keep the utility self‑contained.
    """
    return text.lower().split()


def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the dominant mood in *text*.

    The algorithm:
    1. Tokenize the input.
    2. Count occurrences of each mood's keywords.
    3. Pick the mood with the highest count.
    4. If there is a tie or no matches, return the neutral emoji.
    """
    tokens = _tokenize(text)
    mood_counter = Counter()

    for mood, keywords in MOOD_MAP.items():
        matches = sum(token in keywords for token in tokens)
        if matches:
            mood_counter[mood] = matches

    if not mood_counter:
        return EMOJI_MAP["neutral"]

    # Determine the mood(s) with the highest count
    max_count = max(mood_counter.values())
    top_moods = [m for m, cnt in mood_counter.items() if cnt == max_count]

    if len(top_moods) == 1:
        return EMOJI_MAP[top_moods[0]]
    # Tie – fall back to neutral
    return EMOJI_MAP["neutral"]


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Map a short text to a mood emoji.")
    parser.add_argument("text", nargs="?", help="Text to analyse. If omitted, reads from stdin.")
    args = parser.parse_args()

    if args.text:
        input_text = args.text
    else:
        # Read from stdin when no positional argument is given
        input_text = sys.stdin.read().strip()

    emoji = get_mood_emoji(input_text)
    print(emoji)


if __name__ == "__main__":
    _cli()
