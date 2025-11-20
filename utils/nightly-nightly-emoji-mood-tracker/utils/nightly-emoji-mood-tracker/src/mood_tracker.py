import argparse
import json
import os
from datetime import datetime
from typing import Dict, Optional

DEFAULT_STORAGE = os.path.expanduser("~/.emoji_mood_tracker.json")


class MoodTracker:
    """Simple JSON‑backed mood logger.

    The JSON structure is a mapping from ISO date strings (YYYY‑MM‑DD) to
    dictionaries containing an ``emoji`` and an optional ``note``.
    """

    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or DEFAULT_STORAGE
        self._data: Dict[str, Dict[str, str]] = {}
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except json.JSONDecodeError:
                # Corrupted file – start fresh
                self._data = {}
        else:
            self._data = {}

    def _save(self) -> None:
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def add_entry(self, date: str, emoji: str, note: Optional[str] = None) -> None:
        """Add or replace an entry for *date*.

        *date* must be an ISO‑format string (YYYY‑MM‑DD). No validation beyond
        format checking is performed – the CLI validates the format.
        """
        entry: Dict[str, str] = {"emoji": emoji}
        if note:
            entry["note"] = note
        self._data[date] = entry
        self._save()

    def get_summary(self, days: int = 7) -> Dict[str, str]:
        """Return a mapping of recent dates to their emojis.

        The *days* window is counted backwards from today (inclusive). Dates
        without entries are omitted.
        """
        today = datetime.utcnow().date()
        start = today - datetime.timedelta(days=days - 1)
        summary: Dict[str, str] = {}
        for date_str, entry in self._data.items():
            try:
                entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                continue  # skip malformed keys
            if start <= entry_date <= today:
                summary[date_str] = entry["emoji"]
        # Sort by date descending for readability
        return dict(sorted(summary.items(), reverse=True))

    def __repr__(self) -> str:
        return f"MoodTracker(storage_path={self.storage_path!r}, entries={len(self._data)})"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emoji Mood Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # `add` command
    add_parser = subparsers.add_parser("add", help="Add a mood entry")
    add_parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    add_parser.add_argument("--emoji", required=True, help="Emoji representing the mood")
    add_parser.add_argument("--note", help="Optional short note")

    # `summary` command
    sum_parser = subparsers.add_parser("summary", help="Show recent mood summary")
    sum_parser.add_argument("--days", type=int, default=7, help="Number of days to include")

    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    tracker = MoodTracker()

    if args.command == "add":
        # Basic validation of date format
        try:
            datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError as e:
            raise SystemExit(f"Invalid date format: {e}")
        tracker.add_entry(args.date, args.emoji, args.note)
        print(f"Added entry for {args.date}: {args.emoji}")
    elif args.command == "summary":
        summary = tracker.get_summary(days=args.days)
        if not summary:
            print("No entries in the requested range.")
            return
        print("Recent mood summary (most recent first):")
        for date, emoji in summary.items():
            print(f"{date}: {emoji}")


if __name__ == "__main__":
    main()
