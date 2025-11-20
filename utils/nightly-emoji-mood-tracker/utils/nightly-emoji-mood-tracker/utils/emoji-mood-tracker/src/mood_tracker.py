import argparse
import collections
import datetime
import json
import os
import sys

DEFAULT_PATH = os.path.expanduser("~/.emoji_mood_log.json")


class MoodTracker:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self.data = self._load()

    def _load(self) -> dict:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add(self, date_str: str, emoji: str) -> None:
        self.data[date_str] = emoji
        self._save()

    def stats(self) -> dict:
        total = len(self.data)
        if total == 0:
            return {"total": 0, "most_common": None, "entries": []}
        counter = collections.Counter(self.data.values())
        most_common = counter.most_common(1)[0][0]
        entries = sorted(self.data.items())
        return {"total": total, "most_common": most_common, "entries": entries}


def parse_date(s: str) -> datetime.date:
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError("date must be YYYY-MM-DD")


def main() -> None:
    parser = argparse.ArgumentParser(prog="emoji-mood-tracker")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    add_parser = subparsers.add_parser("add", help="Add a mood entry")
    add_parser.add_argument("emoji", help="Emoji representing your mood")
    add_parser.add_argument("--date", type=parse_date, help="Date for the entry (YYYY-MM-DD)")

    subparsers.add_parser("stats", help="Show statistics")

    args = parser.parse_args()
    tracker = MoodTracker()

    if args.cmd == "add":
        date = args.date or datetime.date.today()
        tracker.add(date.isoformat(), args.emoji)
        print(f"Added {args.emoji} for {date.isoformat()}")
    elif args.cmd == "stats":
        s = tracker.stats()
        print(f"Total entries: {s['total']}")
        if s['total']:
            print(f"Most common emoji: {s['most_common']}")
            print("Chronological entries:")
            for d, e in s['entries']:
                print(f"  {d}: {e}")


if __name__ == "__main__":
    main()
