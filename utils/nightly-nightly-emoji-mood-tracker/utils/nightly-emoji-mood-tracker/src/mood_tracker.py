"""mood_tracker.py

A tiny library + CLI for logging daily moods and retrieving an emoji summary.

The implementation is deliberately simple: a `MoodTracker` class stores entries in an
in‑memory dictionary. The CLI persists data to a JSON file (`~/.emoji_mood_tracker.json`).
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict

# Mapping from mood strings to emojis
MOOD_EMOJI_MAP: Dict[str, str] = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "neutral": "😐",
}

DATA_FILE = Path.home() / ".emoji_mood_tracker.json"


class MoodTracker:
    """Core class handling mood entries.

    The class is deliberately lightweight – it only stores a mapping from ISO‑date
    strings (``YYYY-MM-DD``) to one of the supported mood keys.
    """

    def __init__(self, data_path: Path | None = None) -> None:
        self.data_path = data_path or DATA_FILE
        self.entries: Dict[str, str] = {}
        self._load()

    # ---------------------------------------------------------------------
    # Persistence helpers
    # ---------------------------------------------------------------------
    def _load(self) -> None:
        """Load persisted entries from ``self.data_path`` if the file exists.

        # Mock rationale: In tests we replace the file path with a temporary one,
        # ensuring no real user data is touched.
        """
        if self.data_path.is_file():
            try:
                with self.data_path.open("r", encoding="utf-8") as f:
                    raw = json.load(f)
                # Validate that loaded data conforms to expected shape
                if isinstance(raw, dict):
                    self.entries = {k: v for k, v in raw.items() if v in MOOD_EMOJI_MAP}
            except Exception:
                # Corrupted file – start fresh
                self.entries = {}

    def _save(self) -> None:
        """Persist ``self.entries`` to ``self.data_path``.

        # Mock rationale: Tests mock ``_save`` to avoid filesystem writes.
        """
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with self.data_path.open("w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def add_entry(self, date_str: str, mood: str) -> None:
        """Add or update a mood entry for ``date_str``.

        Args:
            date_str: ISO‑date string (e.g., ``2025-11-29``).
            mood: One of the keys in ``MOOD_EMOJI_MAP``.
        """
        if mood not in MOOD_EMOJI_MAP:
            raise ValueError(f"Unsupported mood '{mood}'. Supported: {list(MOOD_EMOJI_MAP)}")
        # Validate date format
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("date must be in YYYY-MM-DD format") from exc
        self.entries[date_str] = mood
        self._save()

    def get_emoji(self, date_str: str) -> str:
        """Return the emoji for the given date, or a placeholder if unknown.
        """
        mood = self.entries.get(date_str)
        return MOOD_EMOJI_MAP.get(mood, "❓")

    def summary(self) -> str:
        """Return a space‑separated string of emojis sorted by date.
        """
        parts = []
        for date in sorted(self.entries):
            parts.append(self.get_emoji(date))
        return " ".join(parts) if parts else "(no entries)"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nightly_emoji_mood_tracker", description="Log moods and view emoji summaries.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add command
    add_parser = subparsers.add_parser("add", help="Add a mood entry for a date")
    add_parser.add_argument("date", help="Date in YYYY-MM-DD format")
    add_parser.add_argument("mood", choices=MOOD_EMOJI_MAP.keys(), help="Mood to record")

    # show command
    show_parser = subparsers.add_parser("show", help="Show the emoji for a specific date")
    show_parser.add_argument("date", help="Date in YYYY-MM-DD format")

    # summary command
    subparsers.add_parser("summary", help="Print an emoji summary of all entries")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    tracker = MoodTracker()

    if args.command == "add":
        tracker.add_entry(args.date, args.mood)
        print(f"Added {args.mood!r} for {args.date}")
    elif args.command == "show":
        emoji = tracker.get_emoji(args.date)
        print(f"{args.date}: {emoji}")
    elif args.command == "summary":
        print(tracker.summary())


if __name__ == "__main__":
    main()
