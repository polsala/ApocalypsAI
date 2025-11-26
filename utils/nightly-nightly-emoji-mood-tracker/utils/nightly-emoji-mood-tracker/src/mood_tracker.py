import argparse
import datetime
import json
import pathlib
import sys
from collections import Counter
from typing import Dict, Optional


class MoodTracker:
    """Simple emoji‑based mood logger.

    Data is persisted as a JSON mapping of ISO‑date strings to emoji strings.
    """

    def __init__(self, storage_path: Optional[pathlib.Path] = None):
        self.storage_path = storage_path or pathlib.Path.cwd() / ".mood_log.json"
        self._load()

    def _load(self) -> None:
        if self.storage_path.is_file():
            with self.storage_path.open("r", encoding="utf-8") as f:
                self.entries: Dict[str, str] = json.load(f)
        else:
            self.entries = {}

    def _save(self) -> None:
        with self.storage_path.open("w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

    def add_entry(self, date: str, emoji: str) -> None:
        """Add or update the mood for *date* (ISO format ``YYYY‑MM‑DD``)."""
        # Basic validation – keep it lightweight.
        try:
            datetime.date.fromisoformat(date)
        except ValueError as exc:
            raise ValueError(f"Invalid date '{date}'. Use ISO format YYYY-MM-DD.") from exc
        if not emoji:
            raise ValueError("Emoji string cannot be empty.")
        self.entries[date] = emoji
        self._save()

    def get_summary(self, days: int = 7) -> Dict[str, str]:
        """Return a mapping of the most recent *days* dates to their emojis.

        Dates without entries are omitted.
        """
        today = datetime.date.today()
        summary: Dict[str, str] = {}
        for i in range(days):
            d = today - datetime.timedelta(days=i)
            d_str = d.isoformat()
            if d_str in self.entries:
                summary[d_str] = self.entries[d_str]
        return summary

    def most_common(self, days: int = 7) -> str:
        """Return the emoji that appears most frequently in the last *days* days.

        Returns an empty string if no entries exist in the window.
        """
        recent = self.get_summary(days)
        if not recent:
            return ""
        counter = Counter(recent.values())
        return counter.most_common(1)[0][0]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Emoji Mood Tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    # add command
    add_parser = sub.add_parser("add", help="Add or update a mood entry")
    add_parser.add_argument("date", help="Date in ISO format (YYYY-MM-DD)")
    add_parser.add_argument("emoji", help="Emoji representing the mood")

    # summary command
    sum_parser = sub.add_parser("summary", help="Show recent mood summary")
    sum_parser.add_argument("--days", type=int, default=7, help="Number of days to include")

    # common command
    com_parser = sub.add_parser("common", help="Show most common mood in recent days")
    com_parser.add_argument("--days", type=int, default=7, help="Number of days to include")

    return parser


def main(argv: Optional[list] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    tracker = MoodTracker()

    if args.command == "add":
        try:
            tracker.add_entry(args.date, args.emoji)
            print(f"Added mood for {args.date}: {args.emoji}")
        except ValueError as e:
            print(e, file=sys.stderr)
            return 1
    elif args.command == "summary":
        summary = tracker.get_summary(days=args.days)
        if not summary:
            print("No entries in the requested range.")
        else:
            for d, e in sorted(summary.items()):
                print(f"{d}: {e}")
    elif args.command == "common":
        common = tracker.most_common(days=args.days)
        if common:
            print(f"Most common mood in last {args.days} days: {common}")
        else:
            print("No entries to compute most common mood.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
