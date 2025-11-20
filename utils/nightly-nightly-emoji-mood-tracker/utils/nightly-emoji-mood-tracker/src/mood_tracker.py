"""
Emoji Mood Tracker utility.

Provides a simple API to record, retrieve, and analyze daily moods represented by emojis.
Data is persisted in a JSON file mapping ISO date strings to emoji strings.
"""

import json
from pathlib import Path
from datetime import date
from collections import Counter
from typing import Dict, Optional, Tuple


class MoodTracker:
    """Manage emoji moods stored in a JSON file."""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self._data: Dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        if self.storage_path.is_file():
            try:
                self._data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                # Mock rationale: corrupted file should not crash the utility; start fresh.
                self._data = {}
        else:
            self._data = {}

    def _save(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.storage_path.write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def set_mood(self, on_date: date, emoji: str) -> None:
        """Record an emoji for a given date."""
        self._data[on_date.isoformat()] = emoji
        self._save()

    def get_mood(self, on_date: date) -> Optional[str]:
        """Retrieve the emoji for a given date, or None if not recorded."""
        return self._data.get(on_date.isoformat())

    def most_common(self) -> Optional[Tuple[str, int]]:
        """Return the most common emoji and its count, or None if no data."""
        if not self._data:
            return None
        counter = Counter(self._data.values())
        emoji, cnt = counter.most_common(1)[0]
        return emoji, cnt

    def longest_streak(self) -> int:
        """Return the length of the longest consecutive‑day streak with any recorded mood."""
        if not self._data:
            return 0
        dates = sorted(date.fromisoformat(d) for d in self._data.keys())
        longest = current = 1
        for prev, cur in zip(dates, dates[1:]):
            if (cur - prev).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        return longest
