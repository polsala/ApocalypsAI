"""
emoji_mood_tracker.tracker

Provides a simple JSON‑backed mood logger.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

DEFAULT_DB_PATH = os.path.join(os.path.expanduser("~"), ".emoji_mood_tracker.json")


class MoodTracker:
    """Log moods (emoji strings) per date and retrieve weekly summaries."""

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self._data: Dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        """Load the JSON database if it exists."""
        if os.path.exists(self.db_path):
            with open(self.db_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data = {}

    def _save(self) -> None:
        """Persist the in‑memory data to disk."""
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def add_entry(self, date: str, emoji: str) -> None:
        """
        Record a mood for a given ISO date (YYYY‑MM‑DD).

        Overwrites any existing entry for the same date.
        """
        # Validate date format – will raise ValueError if malformed
        datetime.strptime(date, "%Y-%m-%d")
        self._data[date] = emoji
        self._save()

    def get_week_summary(self, start_date: str) -> List[Tuple[str, str]]:
        """
        Return a list of (date, emoji) for the 7‑day window starting at ``start_date``.
        Missing days are represented with an empty string.
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        summary: List[Tuple[str, str]] = []
        for i in range(7):
            day = (start + timedelta(days=i)).strftime("%Y-%m-%d")
            summary.append((day, self._data.get(day, "")))
        return summary


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Emoji Mood Tracker")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    add_parser = subparsers.add_parser("add", help="Add a mood entry")
    add_parser.add_argument("date", help="Date in YYYY-MM-DD")
    add_parser.add_argument("emoji", help="Emoji representing your mood")

    sum_parser = subparsers.add_parser("summary", help="Weekly summary")
    sum_parser.add_argument("start_date", help="Start date of the week (YYYY-MM-DD)")

    args = parser.parse_args()
    tracker = MoodTracker()

    if args.cmd == "add":
        tracker.add_entry(args.date, args.emoji)
        print(f"Recorded {args.emoji} for {args.date}")
    else:  # summary
        week = tracker.get_week_summary(args.start_date)
        for d, e in week:
            print(f"{d}: {e or '(no entry)'}")
