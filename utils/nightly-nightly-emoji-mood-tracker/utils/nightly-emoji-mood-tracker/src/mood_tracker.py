#!/usr/bin/env python3
"""
Emoji Mood Tracker

A simple CLI to record your daily mood using an emoji and view a summary.
Data is stored in a JSON file at `~/.emoji_mood_tracker.json`.
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict

# Default location for the JSON store – can be overridden in tests via monkey‑patching.
DATA_FILE = os.path.expanduser("~/.emoji_mood_tracker.json")


def get_data_path() -> str:
    """Return the path to the JSON data file.
    # Mock rationale: tests replace this function to point at a temporary file.
    """
    return DATA_FILE


def load_data() -> Dict[str, str]:
    """Load mood data from the JSON file.
    Returns an empty dict if the file does not exist or is malformed.
    """
    path = get_data_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_data(data: Dict[str, str]) -> None:
    """Save mood data to the JSON file.
    """
    path = get_data_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_mood(emoji: str, date: str | None = None) -> None:
    """Add or update the mood for a given date (YYYY-MM-DD).
    If *date* is omitted, the current UTC date is used.
    """
    if date is None:
        date = datetime.utcnow().date().isoformat()
    data = load_data()
    data[date] = emoji
    save_data(data)


def get_summary() -> Dict[str, int]:
    """Return a count of each emoji recorded.
    """
    data = load_data()
    summary: Dict[str, int] = {}
    for emoji in data.values():
        summary[emoji] = summary.get(emoji, 0) + 1
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Emoji Mood Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add or update mood for a date")
    add_parser.add_argument("emoji", help="Emoji representing your mood")
    add_parser.add_argument(
        "--date",
        help="Date in YYYY-MM-DD (default: today UTC)",
    )

    subparsers.add_parser("summary", help="Show emoji mood summary")

    args = parser.parse_args()
    if args.command == "add":
        add_mood(args.emoji, args.date)
        print(
            f"Recorded mood {args.emoji} for {args.date or datetime.utcnow().date().isoformat()}"
        )
    elif args.command == "summary":
        summary = get_summary()
        if not summary:
            print("No moods recorded yet.")
        else:
            for emoji, count in sorted(summary.items(), key=lambda x: -x[1]):
                print(f"{emoji}: {count}")


if __name__ == "__main__":
    main()
