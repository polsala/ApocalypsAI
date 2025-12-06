#!/usr/bin/env python3
"""
Emoji Mood Tracker CLI.

Stores daily mood entries (emoji) in a JSON file under the user's home directory.
Provides commands to add a mood, view a summary, and render a simple bar chart.
"""

import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Dict

DATA_FILE = Path.home() / ".emoji_mood_tracker.json"


def load_data() -> Dict[str, str]:
    """Load mood data from the JSON file."""
    if not DATA_FILE.exists():
        return {}
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # Corrupted file – start fresh
        return {}


def save_data(data: Dict[str, str]) -> None:
    """Write mood data to the JSON file."""
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def add_mood(emoji: str) -> None:
    """Record today's mood."""
    today = date.today().isoformat()
    data = load_data()
    data[today] = emoji
    save_data(data)
    print(f"Recorded mood for {today}: {emoji}")


def get_summary() -> Counter:
    """Return a Counter of emoji frequencies."""
    data = load_data()
    return Counter(data.values())


def print_summary() -> None:
    """Print a plain-text summary of emoji counts."""
    summary = get_summary()
    if not summary:
        print("No mood data recorded yet.")
        return
    for emoji, count in summary.most_common():
        print(f"{emoji}: {count}")


def print_chart() -> None:
    """Print a simple bar chart of emoji frequencies."""
    summary = get_summary()
    if not summary:
        print("No mood data recorded yet.")
        return
    max_len = max(len(emoji) for emoji in summary)
    max_count = max(summary.values())
    scale = max_count / 40 if max_count > 40 else 1  # limit width to ~40 chars
    for emoji, count in summary.most_common():
        bar_len = int(count / scale)
        bar = "█" * bar_len
        print(f"{emoji.ljust(max_len)} | {bar} ({count})")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="emoji-mood-tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Record today's mood")
    add_parser.add_argument("emoji", help="Emoji representing your mood")

    subparsers.add_parser("summary", help="Show emoji frequency summary")
    subparsers.add_parser("chart", help="Display a bar chart of moods")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "add":
        add_mood(args.emoji)
    elif args.command == "summary":
        print_summary()
    elif args.command == "chart":
        print_chart()
    else:
        parser.error("Unknown command")
    return 0


if __name__ == "__main__":
    sys.exit(main())
