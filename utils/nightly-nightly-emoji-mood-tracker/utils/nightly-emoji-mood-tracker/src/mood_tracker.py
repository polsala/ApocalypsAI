import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Dict

DATA_FILE = Path.home() / ".emoji_mood_tracker.json"


def _load_data() -> Dict[str, str]:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text())
        except json.JSONDecodeError:
            # Corrupted file – start fresh
            return {}
    return {}


def _save_data(data: Dict[str, str]) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2, sort_keys=True))


def add_mood(emoji: str, on_date: str | None = None) -> None:
    """Record *emoji* for *on_date* (ISO string). If *on_date* is None, use today.
    """
    if on_date is None:
        on_date = date.today().isoformat()
    data = _load_data()
    data[on_date] = emoji
    _save_data(data)
    print(f"Recorded {emoji} for {on_date}")


def show_summary() -> None:
    data = _load_data()
    if not data:
        print("No mood data recorded yet.")
        return
    counter = Counter(data.values())
    total = sum(counter.values())
    print("Mood histogram:")
    for emo, cnt in counter.most_common():
        pct = (cnt / total) * 100
        print(f"{emo} : {cnt} ({pct:.1f}%)")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mood_tracker", description="Record and view emoji moods.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add today's mood.")
    add_parser.add_argument("emoji", help="Emoji representing your mood.")
    add_parser.add_argument("--date", help="ISO date (YYYY-MM-DD). Defaults to today.")

    subparsers.add_parser("show", help="Show mood histogram.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "add":
        add_mood(args.emoji, args.date)
    elif args.command == "show":
        show_summary()
    else:
        parser.error("Unknown command")
    return 0


if __name__ == "__main__":
    sys.exit(main())
