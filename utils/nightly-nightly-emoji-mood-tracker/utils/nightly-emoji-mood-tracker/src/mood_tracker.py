import argparse
import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

DATA_FILE = Path.home() / ".emoji_mood.json"


def _load_data() -> Dict[str, str]:
    """Load the mood JSON file.

    Returns:
        A mapping of ISO date strings to emoji strings.
    """
    if not DATA_FILE.exists():
        return {}
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Corrupted file – start fresh
        return {}


def _save_data(data: Dict[str, str]) -> None:
    """Write the mood mapping back to disk."""
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def log_mood(date_str: str, emoji: str) -> None:
    """Record an emoji mood for a given date.

    Args:
        date_str: ISO date string (YYYY‑MM‑DD). If empty, uses today.
        emoji: The emoji representing the mood.
    """
    if not date_str:
        date_str = datetime.utcnow().date().isoformat()
    else:
        # Validate date format – will raise ValueError if invalid
        datetime.strptime(date_str, "%Y-%m-%d")
    data = _load_data()
    data[date_str] = emoji
    _save_data(data)
    print(f"Logged {emoji} for {date_str}")


def summary() -> Tuple[Counter, int]:
    """Return a Counter of emoji frequencies and total entries.

    Returns:
        (counter, total) where ``counter`` maps emoji → count.
    """
    data = _load_data()
    counter = Counter(data.values())
    total = len(data)
    return counter, total


def _print_summary() -> None:
    counter, total = summary()
    if total == 0:
        print("No mood entries recorded yet.")
        return
    print(f"Total entries: {total}\n")
    for emoji, cnt in counter.most_common():
        print(f"{emoji} : {cnt}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Emoji Mood Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # log subcommand
    log_parser = subparsers.add_parser("log", help="Log a mood for a date")
    log_parser.add_argument("emoji", help="Emoji representing your mood")
    log_parser.add_argument(
        "date",
        nargs="?",
        default="",
        help="Date in YYYY-MM-DD (defaults to today)",
    )

    # summary subcommand
    subparsers.add_parser("summary", help="Show mood summary")
    return parser


def main(argv: List[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "log":
        log_mood(args.date, args.emoji)
    elif args.command == "summary":
        _print_summary()


if __name__ == "__main__":
    main()
