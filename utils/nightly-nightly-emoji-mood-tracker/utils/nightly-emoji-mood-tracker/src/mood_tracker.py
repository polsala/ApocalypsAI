import argparse
import datetime
import json
import pathlib
import sys
from typing import Dict, Optional


class MoodTracker:
    """Simple emoji‑based mood logger.

    Data is persisted as a JSON mapping of ISO‑date strings to emoji strings.
    """

    def __init__(self, storage_path: Optional[pathlib.Path] = None):
        self.storage_path = storage_path or pathlib.Path.home() / ".emoji_mood_tracker.json"
        self._load()

    def _load(self) -> None:
        if self.storage_path.exists():
            try:
                with self.storage_path.open("r", encoding="utf-8") as f:
                    self._data: Dict[str, str] = json.load(f)
            except json.JSONDecodeError:
                # Corrupted file – start fresh
                self._data = {}
        else:
            self._data = {}

    def _save(self) -> None:
        with self.storage_path.open("w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def add_entry(self, date: datetime.date, emoji: str) -> None:
        """Record *emoji* for *date* (overwrites existing entry)."""
        self._data[date.isoformat()] = emoji
        self._save()

    def get_entry(self, date: datetime.date) -> Optional[str]:
        return self._data.get(date.isoformat())

    def summary(self, start: datetime.date, end: datetime.date) -> Dict[str, int]:
        """Return a mapping of emoji → occurrence count between *start* and *end* (inclusive)."""
        counts: Dict[str, int] = {}
        for iso_date, emoji in self._data.items():
            try:
                d = datetime.date.fromisoformat(iso_date)
            except ValueError:
                # Skip malformed keys – should not happen
                continue
            if start <= d <= end:
                counts[emoji] = counts.get(emoji, 0) + 1
        return counts


def _parse_date(s: str) -> datetime.date:
    try:
        return datetime.date.fromisoformat(s)
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid date '{s}'. Expected YYYY-MM-DD.") from e


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(prog="emoji-mood-tracker", description="Log and summarize daily moods using emojis.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add command
    add_parser = subparsers.add_parser("add", help="Add a mood entry.")
    add_parser.add_argument("emoji", help="Emoji representing your mood.")
    add_parser.add_argument("date", nargs="?", type=_parse_date, default=datetime.date.today(), help="Date for the entry (default: today) in YYYY-MM-DD.")

    # summary command
    sum_parser = subparsers.add_parser("summary", help="Show emoji frequency between two dates.")
    sum_parser.add_argument("start", type=_parse_date, help="Start date (inclusive) in YYYY-MM-DD.")
    sum_parser.add_argument("end", type=_parse_date, help="End date (inclusive) in YYYY-MM-DD.")

    args = parser.parse_args(argv)
    tracker = MoodTracker()

    if args.command == "add":
        tracker.add_entry(args.date, args.emoji)
        print(f"Added entry for {args.date.isoformat()}: {args.emoji}")
    elif args.command == "summary":
        if args.start > args.end:
            parser.error("Start date must not be after end date.")
        result = tracker.summary(args.start, args.end)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        parser.error("Unknown command")

    return 0


if __name__ == "__main__":
    sys.exit(main())
