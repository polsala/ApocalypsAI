#!/usr/bin/env python3
"""
emoji mood tracker utility
"""

import json
import sys
from pathlib import Path
from collections import Counter
from typing import Dict, List, Tuple

# Path to the JSON file that stores mood entries (same directory as this script)
DATA_FILE = Path(__file__).with_name("mood_data.json")


def load_data() -> List[Tuple[str, str]]:
    """Load the list of (date, emoji) entries from the JSON file.

    Returns an empty list if the file does not exist.
    """
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_data(entries: List[Tuple[str, str]]) -> None:
    """Persist the list of entries to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def add_entry(date: str, emoji: str) -> None:
    """Add or replace an entry for *date* with the given *emoji*.

    If an entry for the same date already exists it is overwritten.
    """
    entries = load_data()
    # Remove any existing entry for the same date
    entries = [e for e in entries if e[0] != date]
    entries.append((date, emoji))
    save_data(entries)


def summary() -> Dict[str, int]:
    """Return a dictionary mapping each emoji to the number of times it appears."""
    entries = load_data()
    counter = Counter(emoji for _, emoji in entries)
    return dict(counter)


def cli() -> None:
    """Simple command‑line interface.

    Commands:
        add <date> <emoji>   – record a mood for a specific date (ISO format)
        summary              – print a count of each recorded emoji
    """
    if len(sys.argv) < 2:
        print("Usage: mood_tracker add <date> <emoji> | summary")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) == 4:
        _, _, date, emoji = sys.argv
        add_entry(date, emoji)
        print(f"Added {emoji} for {date}")
    elif cmd == "summary":
        stats = summary()
        if not stats:
            print("No entries yet.")
        else:
            for emoji, count in sorted(stats.items(), key=lambda x: -x[1]):
                print(f"{emoji}: {count}")
    else:
        print("Invalid command.")
        sys.exit(1)


if __name__ == "__main__":
    cli()
