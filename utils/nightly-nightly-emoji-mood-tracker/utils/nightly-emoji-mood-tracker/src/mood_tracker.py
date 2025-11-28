import argparse
import json
import os
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Any

DEFAULT_DB_PATH = Path.home() / ".emoji_mood_tracker.json"


def load_db(db_path: Path = DEFAULT_DB_PATH) -> Dict[str, str]:
    if db_path.is_file():
        try:
            return json.loads(db_path.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_db(data: Dict[str, str], db_path: Path = DEFAULT_DB_PATH) -> None:
    db_path.write_text(json.dumps(data, indent=2, sort_keys=True))


def log_mood(emoji: str, today: date = None, db_path: Path = DEFAULT_DB_PATH) -> None:
    today = today or date.today()
    data = load_db(db_path)
    data[today.isoformat()] = emoji
    save_db(data, db_path)


def get_summary(days: int = 7, today: date = None, db_path: Path = DEFAULT_DB_PATH) -> List[Dict[str, Any]]:
    today = today or date.today()
    data = load_db(db_path)
    summary = []
    for i in range(days):
        day = today - datetime.timedelta(days=i)
        iso = day.isoformat()
        if iso in data:
            summary.append({"date": iso, "emoji": data[iso]})
    return summary[::-1]  # oldest first


def cli() -> None:
    parser = argparse.ArgumentParser(prog="emoji-mood", description="Log and summarize daily emoji moods.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    log_parser = subparsers.add_parser("log", help="Log today's mood.")
    log_parser.add_argument("emoji", type=str, help="Emoji representing your mood.")

    sum_parser = subparsers.add_parser("summary", help="Show recent mood summary.")
    sum_parser.add_argument("days", type=int, nargs="?", default=7, help="Number of days to include.")

    args = parser.parse_args()
    if args.command == "log":
        log_mood(args.emoji)
        print(f"Logged mood {args.emoji} for today.")
    elif args.command == "summary":
        summary = get_summary(args.days)
        if not summary:
            print("No mood data found.")
            return
        for entry in summary:
            print(f"{entry['date']}: {entry['emoji']}")


if __name__ == "__main__":
    cli()
