import argparse
import json
import os
from collections import Counter
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

# Path to the JSON file that stores mood entries
DATA_FILE = Path.home() / ".mood_tracker.json"


def _load_data() -> Dict[str, str]:
    """Load the mood data from the JSON file.

    Returns:
        A dictionary mapping ISO date strings (YYYY-MM-DD) to emoji strings.
    """
    if not DATA_FILE.exists():
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Corrupted file – start fresh
        return {}


def _save_data(data: Dict[str, str]) -> None:
    """Persist the mood data to the JSON file.

    Args:
        data: Mapping of dates to emojis.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_entry(mood: str, entry_date: str | None = None) -> Tuple[bool, str]:
    """Add a mood entry.

    Args:
        mood: Emoji representing the mood.
        entry_date: Optional ISO date string. If omitted, uses today.

    Returns:
        (created, message) where `created` is True if a new entry was added,
        False if the entry already existed (and was overwritten).
    """
    if entry_date is None:
        entry_date = date.today().isoformat()
    else:
        # Validate date format
        try:
            datetime.strptime(entry_date, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Invalid date format: {entry_date}. Expected YYYY-MM-DD") from e

    data = _load_data()
    created = entry_date not in data
    data[entry_date] = mood
    _save_data(data)
    return created, f"Mood for {entry_date} set to {mood}"


def summary(days: int = 7) -> Dict[str, int]:
    """Return a count of emojis used in the last `days` days.

    Args:
        days: Number of days to look back from today (inclusive).

    Returns:
        A dictionary mapping each emoji to its occurrence count.
    """
    if days <= 0:
        raise ValueError("days must be a positive integer")
    data = _load_data()
    cutoff = date.today() - timedelta(days=days - 1)
    recent_entries = [emoji for d, emoji in data.items() if datetime.strptime(d, "%Y-%m-%d").date() >= cutoff]
    return dict(Counter(recent_entries))


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emoji Mood Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub‑command: add
    add_parser = subparsers.add_parser("add", help="Add a mood entry")
    add_parser.add_argument("emoji", help="Emoji representing your mood")
    add_parser.add_argument("date", nargs="?", help="Date for the entry (YYYY-MM-DD). Defaults to today.")

    # Sub‑command: summary
    sum_parser = subparsers.add_parser("summary", help="Show mood summary for recent days")
    sum_parser.add_argument("days", nargs="?", type=int, default=7, help="Number of days to include (default: 7)")

    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> None:
    args = _parse_args(argv)
    if args.command == "add":
        created, msg = add_entry(args.emoji, args.date)
        print(msg)
    elif args.command == "summary":
        counts = summary(args.days)
        if not counts:
            print("No mood entries found for the requested period.")
            return
        print(f"Mood summary for the last {args.days} day(s):")
        for emoji, cnt in sorted(counts.items(), key=lambda kv: kv[1], reverse=True):
            print(f"{emoji}: {cnt}")


if __name__ == "__main__":
    main()
