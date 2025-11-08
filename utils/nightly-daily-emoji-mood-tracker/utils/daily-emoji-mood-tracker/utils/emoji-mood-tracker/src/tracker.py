import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

LOG_PATH = Path.home() / ".emoji_mood_log.json"


def _load_log(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    return []


def _save_log(path: Path, entries: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def log_mood(emoji: str, note: str = "", today: date = None) -> None:
    today = today or date.today()
    entry = {
        "date": today.isoformat(),
        "emoji": emoji,
        "note": note,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    entries = _load_log(LOG_PATH)
    entries.append(entry)
    _save_log(LOG_PATH, entries)
    print(f"Logged mood for {today}: {emoji} {note}")


def summary(days: int = 7, today: date = None) -> None:
    today = today or date.today()
    start_date = today - timedelta(days=days - 1)
    entries = _load_log(LOG_PATH)
    counts: Dict[str, int] = {}
    for e in entries:
        entry_date = date.fromisoformat(e.get("date", ""))
        if start_date <= entry_date <= today:
            emoji = e.get("emoji", "")
            counts[emoji] = counts.get(emoji, 0) + 1
    if not counts:
        print("No mood entries in the requested period.")
        return
    print(f"Mood summary for the last {days} days (including {today}):")
    for emoji, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"{emoji}: {cnt}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="emoji-mood-tracker", description="Log and summarize daily moods using emojis.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    log_parser = subparsers.add_parser("log", help="Log today’s mood.")
    log_parser.add_argument("emoji", help="Emoji representing your mood.")
    log_parser.add_argument("note", nargs="?", default="", help="Optional short note.")

    sum_parser = subparsers.add_parser("summary", help="Show a summary of recent moods.")
    sum_parser.add_argument("-d", "--days", type=int, default=7, help="Number of days to include in the summary (default: 7).")
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "log":
        log_mood(args.emoji, args.note)
    elif args.command == "summary":
        summary(days=args.days)
    else:
        parser.error("Unknown command")
    return 0


if __name__ == "__main__":
    sys.exit(main())
