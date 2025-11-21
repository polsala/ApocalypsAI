import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import List, Dict

DEFAULT_LOG_FILENAME = ".emoji_mood_log.json"


def _log_path() -> Path:
    """Return the path to the JSON log file.

    The location can be overridden with the ``EMOJI_MOOD_LOG`` environment variable.
    """
    env_path = os.getenv("EMOJI_MOOD_LOG")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return Path.cwd() / DEFAULT_LOG_FILENAME


def _load_entries() -> List[str]:
    """Load the list of stored emoji entries.

    Returns an empty list if the file does not exist or is malformed.
    """
    path = _log_path()
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [str(item) for item in data]
    except Exception:
        # Mock rationale: tolerate any read/parse error and start fresh.
        return []
    return []


def _save_entries(entries: List[str]) -> None:
    """Persist the list of emoji entries to disk."""
    path = _log_path()
    path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")


def add_entry(emoji: str) -> None:
    """Add a single emoji entry to the log.

    Args:
        emoji: The emoji string to record.
    """
    if not emoji:
        raise ValueError("Emoji cannot be empty")
    entries = _load_entries()
    entries.append(emoji)
    _save_entries(entries)
    print(f"Recorded mood: {emoji}")


def summary() -> Dict[str, int]:
    """Return a dictionary mapping each emoji to its occurrence count."""
    entries = _load_entries()
    counter = Counter(entries)
    return dict(counter)


def _print_summary() -> None:
    stats = summary()
    if not stats:
        print("No mood entries recorded yet.")
        return
    print("Emoji Mood Summary:")
    for emoji, count in sorted(stats.items(), key=lambda kv: kv[1], reverse=True):
        print(f"{emoji}: {count}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Emoji Mood Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a mood entry")
    add_parser.add_argument("emoji", type=str, help="Emoji representing your mood")

    subparsers.add_parser("summary", help="Show a summary of recorded moods")
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "add":
            add_entry(args.emoji)
        elif args.command == "summary":
            _print_summary()
        else:
            parser.error("Unknown command")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
