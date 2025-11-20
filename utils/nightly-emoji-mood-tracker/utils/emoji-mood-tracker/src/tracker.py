import argparse
import json
import os
from collections import Counter
from datetime import date
from typing import Dict, List, Tuple

LOG_FILE = "mood_log.json"


def _load_log() -> Dict[str, List[str]]:
    """Load the mood log from disk.

    Returns a mapping of ISO date strings to a list of emojis recorded for that day.
    """
    if not os.path.exists(LOG_FILE):
        return {}
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_log(log: Dict[str, List[str]]) -> None:
    """Persist the mood log to disk."""
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def add_mood(emoji: str, on_date: date | None = None) -> None:
    """Record an emoji for the given date (defaults to today)."""
    today = (on_date or date.today()).isoformat()
    log = _load_log()
    log.setdefault(today, []).append(emoji)
    _save_log(log)


def get_mood(on_date: date | None = None) -> List[str]:
    """Retrieve the list of emojis recorded for the given date.

    Returns an empty list if no entry exists.
    """
    target = (on_date or date.today()).isoformat()
    log = _load_log()
    return log.get(target, [])


def summary() -> List[Tuple[str, int]]:
    """Return a list of (emoji, count) sorted by count descending."""
    log = _load_log()
    counter = Counter(emoji for emojis in log.values() for emoji in emojis)
    return sorted(counter.items(), key=lambda item: item[1], reverse=True)


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Emoji Mood Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add today's mood")
    add_parser.add_argument("emoji", help="Emoji representing your mood")

    subparsers.add_parser("show", help="Show today's mood")
    subparsers.add_parser("summary", help="Show summary of all moods")

    args = parser.parse_args()

    if args.command == "add":
        add_mood(args.emoji)
        print(f"Recorded mood {args.emoji} for today.")
    elif args.command == "show":
        moods = get_mood()
        if moods:
            print("Today's moods:", " ".join(moods))
        else:
            print("No mood recorded for today.")
    elif args.command == "summary":
        for emoji, count in summary():
            print(f"{emoji}: {count}")


if __name__ == "__main__":
    _cli()
