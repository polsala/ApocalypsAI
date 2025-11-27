import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

DEFAULT_STORAGE = Path.home() / ".emoji_mood_tracker.json"


class MoodTracker:
    """Simple emoji‑based mood logger.

    The data format is a dict mapping ISO‑date strings to emoji strings:
    {
        "2025-11-27": "😊",
        "2025-11-26": "😢",
        ...
    }
    """

    def __init__(self, storage_path: Path | str = DEFAULT_STORAGE):
        self.storage_path = Path(storage_path)
        self._data: Dict[str, str] = {}
        self._load()

    # ---------------------------------------------------------------------
    # Persistence helpers
    # ---------------------------------------------------------------------
    def _load(self) -> None:
        if self.storage_path.is_file():
            try:
                with self.storage_path.open("r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except json.JSONDecodeError:
                # Corrupted file – start fresh
                self._data = {}
        else:
            self._data = {}

    def _save(self) -> None:
        # Ensure parent directory exists (mostly for tests with temp dirs)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with self.storage_path.open("w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def add_entry(self, date_str: str, emoji: str) -> None:
        """Add or update a mood entry.

        Args:
            date_str: ISO‑format date (YYYY‑MM‑DD).
            emoji: A single Unicode emoji representing the mood.
        """
        # Validate date format – will raise ValueError if invalid
        datetime.strptime(date_str, "%Y-%m-%d")
        if not emoji:
            raise ValueError("Emoji cannot be empty")
        self._data[date_str] = emoji
        self._save()

    def get_summary(self) -> Counter:
        """Return a Counter of emoji occurrences.

        Example:
            Counter({"😊": 5, "😢": 2})
        """
        return Counter(self._data.values())

    def list_entries(self) -> List[Tuple[str, str]]:
        """Return a sorted list of (date, emoji) tuples.
        """
        return sorted(self._data.items())


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Log and summarize your daily mood using emojis."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add command
    add_parser = subparsers.add_parser("add", help="Add or update a mood entry")
    add_parser.add_argument("date", help="Date in YYYY-MM-DD format")
    add_parser.add_argument("emoji", help="Emoji representing your mood")

    # summary command
    subparsers.add_parser("summary", help="Show a summary of logged moods")

    # list command (optional, for debugging)
    subparsers.add_parser("list", help="List all logged entries")

    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = _parse_args(argv)
    tracker = MoodTracker()

    if args.command == "add":
        try:
            tracker.add_entry(args.date, args.emoji)
            print(f"✅ Added mood for {args.date}: {args.emoji}")
        except Exception as e:
            print(f"❌ Failed to add entry: {e}", file=sys.stderr)
            return 1
    elif args.command == "summary":
        summary = tracker.get_summary()
        if not summary:
            print("No mood entries found.")
        else:
            print("Mood Summary:")
            for emoji, count in summary.most_common():
                print(f"{emoji} : {count}")
    elif args.command == "list":
        entries = tracker.list_entries()
        if not entries:
            print("No entries logged.")
        else:
            for date, emoji in entries:
                print(f"{date}: {emoji}")
    else:
        # Should never happen due to argparse enforcement
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
