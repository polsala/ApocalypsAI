"""emoji_mood_analyzer

A tiny, dependency‑free module that determines the dominant mood of a text based on a predefined emoji set.

Exported API:
    - ``analyze_mood(text: str) -> str``
        Returns one of ``"happy"``, ``"sad"``, ``"angry"`` or ``"neutral"``.
    - ``main()`` – simple CLI entry point.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from typing import Dict, List

# Mapping of emojis to mood categories
MOOD_EMOJIS: Dict[str, List[str]] = {
    "happy": ["😊", "😄", "😁"],
    "sad": ["😢", "😞", "😔"],
    "angry": ["😠", "😡"],
}

# Reverse lookup for fast counting
EMOJI_TO_MOOD: Dict[str, str] = {
    emoji: mood for mood, emojis in MOOD_EMOJIS.items() for emoji in emojis
}


def _count_emojis(text: str) -> Counter:
    """Count occurrences of known emojis in *text*.

    Returns a ``Counter`` where keys are mood strings and values are counts.
    """
    counts = Counter()
    for char in text:
        mood = EMOJI_TO_MOOD.get(char)
        if mood:
            counts[mood] += 1
    return counts


def analyze_mood(text: str) -> str:
    """Return the dominant mood for *text*.

    The algorithm:
    1. Count known emojis per mood.
    2. If no emojis are found → ``"neutral"``.
    3. Pick the mood with the highest count.
    4. In case of a tie → ``"neutral"``.
    """
    counts = _count_emojis(text)
    if not counts:
        return "neutral"
    # Find the highest count(s)
    max_count = max(counts.values())
    top_moods = [m for m, c in counts.items() if c == max_count]
    if len(top_moods) == 1:
        return top_moods[0]
    # Tie – ambiguous sentiment
    return "neutral"


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect dominant emoji mood in a string or file."
    )
    parser.add_argument(
        "text_or_path",
        help="Raw text to analyze or path to a file containing text.",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store_true",
        help="Interpret the first argument as a file path.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    if args.file:
        try:
            with open(args.text_or_path, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError as exc:
            print(f"Error reading file: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        content = args.text_or_path
    mood = analyze_mood(content)
    print(mood)


if __name__ == "__main__":
    main()
