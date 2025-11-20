#!/usr/bin/env python3
"""
Emoji Mood Tracker

Read a plain‑text file where each line is a mood descriptor.
Aggregate frequencies, pick the most common mood, and output a friendly
emoji summary.

If multiple moods tie for top frequency, all are shown.

Example:
    $ cat moods.txt
    happy
    sad
    happy
    excited
    $ python -m mood_tracker moods.txt
    📈 Mood summary: happy 😊 (2)
"""

import sys
from collections import Counter
from pathlib import Path
from typing import List, Tuple

# Mapping from mood keyword to emoji
MOOD_EMOJI = {
    "happy": "😊",
    "sad": "😢",
    "excited": "🤩",
    "angry": "😠",
    "tired": "😴",
    "anxious": "😰",
    "confused": "🤔",
    "love": "❤️",
    "bored": "😐",
    "surprised": "😲",
}


def load_moods(file_path: Path) -> List[str]:
    """Read moods from a file, stripping whitespace and ignoring blanks."""
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    return [line.strip().lower() for line in file_path.read_text().splitlines() if line.strip()]


def most_common_moods(moods: List[str]) -> List[Tuple[str, int]]:
    """Return a list of (mood, count) for the highest‑frequency moods."""
    if not moods:
        return []
    counter = Counter(moods)
    max_count = max(counter.values())
    return [(mood, cnt) for mood, cnt in counter.items() if cnt == max_count]


def mood_to_emoji(mood: str) -> str:
    """Translate a mood word to an emoji; fallback to the word itself."""
    return MOOD_EMOJI.get(mood, mood)


def format_summary(common: List[Tuple[str, int]]) -> str:
    """Create a human‑readable summary string."""
    parts = [f"{mood} {mood_to_emoji(mood)} ({cnt})" for mood, cnt in common]
    return ", ".join(parts)


def main(argv: List[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m mood_tracker <moods.txt>", file=sys.stderr)
        return 1
    try:
        moods = load_moods(Path(argv[0]))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    common = most_common_moods(moods)
    if not common:
        print("No moods found.")
        return 0

    summary = format_summary(common)
    print(f"📈 Mood summary: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
