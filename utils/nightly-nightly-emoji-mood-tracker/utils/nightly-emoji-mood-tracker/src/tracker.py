"""emoji_mood_tracker

A tiny library that maps textual moods to emojis, stores them by date, and can produce a summary.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field
from typing import Dict, List

_MOOD_EMOJI_MAP: Dict[str, str] = {
    "happy": "😄",
    "sad": "😢",
    "angry": "😠",
    "tired": "😴",
    "excited": "🤩",
    "confused": "🤔",
    "love": "❤️",
    "bored": "😐",
    # fallback for unknown moods
    "default": "🤷",
}

def mood_to_emoji(mood: str) -> str:
    """Return an emoji for *mood*.

    The lookup is case‑insensitive. If the mood is not recognised, a generic
    "shrug" emoji is returned.
    """
    return _MOOD_EMOJI_MAP.get(mood.lower(), _MOOD_EMOJI_MAP["default"])

@dataclass
class MoodEntry:
    date: _dt.date
    mood: str
    emoji: str = field(init=False)

    def __post_init__(self) -> None:
        self.emoji = mood_to_emoji(self.mood)

class MoodTracker:
    """Collects MoodEntry objects and can summarise them.

    All dates are stored as ``datetime.date`` objects. The tracker does not
    persist data to disk – it lives in memory for the duration of the process.
    """

    def __init__(self) -> None:
        self._entries: List[MoodEntry] = []

    def add_mood(self, date_str: str, mood: str) -> None:
        """Add a mood for a given ISO‑format date string (YYYY‑MM‑DD)."""
        try:
            date_obj = _dt.date.fromisoformat(date_str)
        except ValueError as exc:
            raise ValueError(f"Invalid date format: {date_str!r}") from exc
        entry = MoodEntry(date=date_obj, mood=mood)
        self._entries.append(entry)

    def get_summary(self, start_date_str: str, end_date_str: str) -> str:
        """Return a one‑line summary of moods between *start_date* and *end_date* inclusive.

        The format is ``YYYY‑MM‑DD: <emoji>`` per line, sorted chronologically.
        """
        start = _dt.date.fromisoformat(start_date_str)
        end = _dt.date.fromisoformat(end_date_str)
        if start > end:
            raise ValueError("start_date must be on or before end_date")
        filtered = [e for e in self._entries if start <= e.date <= end]
        filtered.sort(key=lambda e: e.date)
        lines = [f"{e.date.isoformat()}: {e.emoji}" for e in filtered]
        return "\n".join(lines) if lines else "No entries in the given range."
