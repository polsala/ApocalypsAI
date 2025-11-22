"""mood_tracker.py

Utility to parse a simple mood log and produce an emoji‑based summary.

The module can be used programmatically via ``load_entries`` and ``summarize``
or as a CLI with ``python -m src.mood_tracker --file <path>``.
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import sys
from typing import Dict, List, Tuple

# Mapping from textual mood to emoji
MOOD_EMOJI: Dict[str, str] = {
    "happy": "😄",
    "sad": "😢",
    "angry": "😠",
    "neutral": "😐",
}


def parse_line(line: str) -> Tuple[str, str]:
    """Parse a single line of the log.

    Expected format: ``YYYY-MM-DD <mood>``.
    Returns a tuple ``(date, mood)``.
    Raises ``ValueError`` if the line is malformed or mood unknown.
    """
    parts = line.strip().split()
    if len(parts) != 2:
        raise ValueError(f"Malformed line: {line!r}")
    date, mood = parts
    if mood not in MOOD_EMOJI:
        raise ValueError(f"Unknown mood '{mood}' in line: {line!r}")
    return date, mood


def load_entries(file_path: str | pathlib.Path) -> List[Tuple[str, str]]:
    """Read the log file and return a list of ``(date, mood)`` tuples.

    The function is deliberately small to ease testing – the file I/O can be
    mocked in the unit tests.
    """
    entries: List[Tuple[str, str]] = []
    path = pathlib.Path(file_path)
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():  # skip empty lines
                entries.append(parse_line(line))
    return entries


def summarize(entries: List[Tuple[str, str]]) -> Dict[str, object]:
    """Create a summary dictionary from parsed entries.

    The returned dict contains:
    - ``total``: total number of entries
    - ``counts``: ``Dict[mood, int]`` of occurrences
    - ``most_common``: ``(mood, emoji, count)`` tuple for the dominant mood
    """
    total = len(entries)
    mood_counter: collections.Counter[str] = collections.Counter(mood for _, mood in entries)
    if mood_counter:
        most_common_mood, most_common_count = mood_counter.most_common(1)[0]
        most_common = (most_common_mood, MOOD_EMOJI[most_common_mood], most_common_count)
    else:
        most_common = ("", "", 0)
    return {
        "total": total,
        "counts": dict(mood_counter),
        "most_common": most_common,
    }


def format_summary(summary: Dict[str, object]) -> str:
    """Render the summary dict as a human‑readable string."""
    lines = [f"Total entries: {summary['total']}"]
    counts: Dict[str, int] = summary["counts"]
    for mood in sorted(MOOD_EMOJI.keys()):
        count = counts.get(mood, 0)
        emoji = MOOD_EMOJI[mood]
        lines.append(f"{mood.ljust(7)} {emoji} : {count}")
    most_mood, most_emoji, most_cnt = summary["most_common"]
    if most_mood:
        lines.append(f"Most common mood: {most_emoji} ({most_mood})")
    else:
        lines.append("Most common mood: N/A")
    return "\n".join(lines)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize a mood log with emojis.")
    parser.add_argument("--file", required=True, help="Path to the mood log file")
    args = parser.parse_args(argv)
    try:
        entries = load_entries(args.file)
        summary = summarize(entries)
        print(format_summary(summary))
        return 0
    except Exception as exc:  # pragma: no cover – CLI error path
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
