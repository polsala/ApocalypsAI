import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, TypedDict

# Path to the JSON log file (hidden in the user's home directory)
LOG_PATH = Path.home() / ".emoji_mood_log.json"


class MoodEntry(TypedDict):
    emoji: str
    note: str
    timestamp: str  # ISO‑8601 date string (YYYY‑MM‑DD)


def _load_log() -> Dict[str, MoodEntry]:
    """Load the JSON log from disk. Returns an empty dict if the file does not exist."""
    if LOG_PATH.exists():
        try:
            with LOG_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure keys are strings and values conform to MoodEntry shape
                return {k: v for k, v in data.items() if isinstance(k, str) and isinstance(v, dict)}
        except json.JSONDecodeError:
            # Corrupted file – start fresh but warn the user
            print(f"[warning] Corrupted log file at {LOG_PATH}, starting with an empty log.", file=sys.stderr)
    return {}


def _save_log(log: Dict[str, MoodEntry]) -> None:
    """Write the log dictionary back to disk atomically."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = LOG_PATH.with_suffix(".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, sort_keys=True)
    tmp_path.replace(LOG_PATH)


def add_mood(entry_date: date, emoji: str, note: str = "") -> None:
    """Add or update a mood entry for *entry_date*.

    Args:
        entry_date: The date the mood applies to.
        emoji: A single Unicode emoji representing the mood.
        note: Optional free‑form text.
    """
    if not emoji:
        raise ValueError("Emoji must be a non‑empty string.")
    log = _load_log()
    key = entry_date.isoformat()
    log[key] = MoodEntry(emoji=emoji, note=note, timestamp=key)
    _save_log(log)
    print(f"✅ Logged mood for {key}: {emoji} {note}")


def get_recent_summary(days: int = 7) -> List[MoodEntry]:
    """Return a list of MoodEntry objects for the most recent *days* (including today).

    The list is ordered from oldest to newest.
    """
    if days <= 0:
        raise ValueError("days must be a positive integer")
    today = date.today()
    start = today - timedelta(days=days - 1)
    log = _load_log()
    entries: List[MoodEntry] = []
    for i in range(days):
        cur = (start + timedelta(days=i)).isoformat()
        if cur in log:
            entries.append(log[cur])
    return entries


def _print_summary(days: int) -> None:
    entries = get_recent_summary(days)
    if not entries:
        print("No mood entries found for the requested period.")
        return
    print(f"Mood summary for the last {days} day(s):")
    for entry in entries:
        ts = entry["timestamp"]
        emoji = entry["emoji"]
        note = entry["note"]
        note_part = f" – {note}" if note else ""
        print(f"{ts}: {emoji}{note_part}")


def _parse_date(s: str) -> date:
    """Parse a string into a date. Accepts 'YYYY-MM-DD' or the literal 'today'."""
    if s.lower() == "today":
        return date.today()
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date format: {s!r}. Expected YYYY-MM-DD or 'today'.") from exc


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(prog="mood_tracker", description="Log and view emoji‑based mood entries.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub‑command: add
    add_parser = subparsers.add_parser("add", help="Add or update a mood entry.")
    add_parser.add_argument("date_or_emoji", help="Either an emoji (for today) or a date in YYYY‑MM‑DD.")
    add_parser.add_argument("emoji", nargs="?", help="Emoji representing the mood (omit if first arg is a date).")
    add_parser.add_argument("note", nargs="*", help="Optional free‑form note (may contain spaces).")

    # Sub‑command: summary
    sum_parser = subparsers.add_parser("summary", help="Show a summary of recent moods.")
    sum_parser.add_argument("days", type=int, nargs="?", default=7, help="Number of days to include (default: 7).")

    args = parser.parse_args(argv)

    if args.command == "add":
        # Determine if first positional is a date or an emoji
        try:
            possible_date = _parse_date(args.date_or_emoji)
            # First arg is a date, second must be emoji
            if not args.emoji:
                parser.error("When providing a date, you must also supply an emoji.")
            entry_date = possible_date
            emoji = args.emoji
        except argparse.ArgumentTypeError:
            # First arg is an emoji, date defaults to today
            entry_date = date.today()
            emoji = args.date_or_emoji
        note = " ".join(args.note) if args.note else ""
        add_mood(entry_date, emoji, note)
    elif args.command == "summary":
        _print_summary(args.days)
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()
