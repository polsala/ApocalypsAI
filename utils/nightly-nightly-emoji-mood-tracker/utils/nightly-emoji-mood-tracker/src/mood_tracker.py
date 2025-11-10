"""
Emoji Mood Tracker

Provides functions to add a mood entry (emoji) for the current date and
to compute a summary of recorded moods.

The data is stored in a JSON file (default: "mood_log.json") with the
structure:
{
    "YYYY-MM-DD": ["😊", "😢", ...],
    ...
}
"""

import argparse
import json
import os
from datetime import date
from collections import Counter
from typing import Dict, List

DEFAULT_LOG = "mood_log.json"


def _load_log(path: str) -> Dict[str, List[str]]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_log(log: Dict[str, List[str]], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def add_mood(emoji: str, log_path: str = DEFAULT_LOG, today: date = None) -> None:
    """Record *emoji* for *today* (or supplied date) in *log_path*.
    """
    today = today or date.today()
    key = today.isoformat()
    log = _load_log(log_path)
    log.setdefault(key, []).append(emoji)
    _save_log(log, log_path)


def get_summary(log_path: str = DEFAULT_LOG) -> Counter:
    """Return a Counter mapping each emoji to its total occurrences.
    """
    log = _load_log(log_path)
    counter = Counter()
    for emojis in log.values():
        counter.update(emojis)
    return counter


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Emoji Mood Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a mood emoji for today")
    add_parser.add_argument("emoji", help="Emoji representing your mood")

    subparsers.add_parser("summary", help="Show aggregated mood counts")

    args = parser.parse_args()
    if args.command == "add":
        add_mood(args.emoji)
        print(f"Added mood {args.emoji}")
    elif args.command == "summary":
        summary = get_summary()
        if not summary:
            print("No moods recorded yet.")
        else:
            for emo, cnt in summary.most_common():
                print(f"{emo}: {cnt}")


if __name__ == "__main__":
    _cli()
