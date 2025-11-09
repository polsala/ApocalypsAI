import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Default storage location – can be overridden via the DAILY_EMOJI_MOOD_PATH env var
DEFAULT_STORAGE = Path.home() / ".local" / "share" / "daily_emoji_mood_tracker.json"


def _storage_path() -> Path:
    """Resolve the JSON storage path, respecting the environment variable.

    Returns:
        Path: Path object pointing to the JSON file.
    """
    env_path = os.getenv("DAILY_EMOJI_MOOD_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return DEFAULT_STORAGE


def _load_data() -> List[Dict[str, Any]]:
    """Load the mood entries from the JSON file.

    Returns:
        List[Dict[str, Any]]: List of entry dictionaries.
    """
    path = _storage_path()
    if not path.is_file():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Corrupted file – start fresh
        return []


def _save_data(entries: List[Dict[str, Any]]) -> None:
    """Persist the list of entries to the JSON file.

    Args:
        entries (List[Dict[str, Any]]): The mood entries to store.
    """
    path = _storage_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def log_mood(emoji: str, note: str = "") -> None:
    """Add a new mood entry.

    Args:
        emoji (str): Emoji representing the mood.
        note (str, optional): Optional free‑form note. Defaults to "".
    """
    if not emoji:
        raise ValueError("Emoji must be provided for a mood entry.")
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "emoji": emoji,
        "note": note,
    }
    entries = _load_data()
    entries.append(entry)
    _save_data(entries)
    print(f"Logged mood: {emoji} {note}")


def get_summary(last: int = 5) -> List[Dict[str, Any]]:
    """Return the most recent *last* entries.

    Args:
        last (int, optional): Number of recent entries to return. Defaults to 5.

    Returns:
        List[Dict[str, Any]]: List of entry dictionaries ordered newest first.
    """
    entries = _load_data()
    return list(reversed(entries))[:last]


def _print_summary(entries: List[Dict[str, Any]]) -> None:
    if not entries:
        print("No mood entries found.")
        return
    for e in entries:
        ts = e["timestamp"]
        emoji = e["emoji"]
        note = e["note"]
        note_part = f" – {note}" if note else ""
        print(f"{ts}: {emoji}{note_part}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="daily_emoji_mood_tracker",
        description="Log and view daily mood entries using emojis.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # log command
    log_parser = subparsers.add_parser("log", help="Record a new mood entry.")
    log_parser.add_argument("emoji", help="Emoji representing your mood.")
    log_parser.add_argument("note", nargs="?", default="", help="Optional note.")

    # summary command
    sum_parser = subparsers.add_parser("summary", help="Show recent mood entries.")
    sum_parser.add_argument(
        "--last",
        type=int,
        default=5,
        help="Number of recent entries to display (default: 5).",
    )
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "log":
        try:
            log_mood(args.emoji, args.note)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    elif args.command == "summary":
        entries = get_summary(args.last)
        _print_summary(entries)
    else:
        parser.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
