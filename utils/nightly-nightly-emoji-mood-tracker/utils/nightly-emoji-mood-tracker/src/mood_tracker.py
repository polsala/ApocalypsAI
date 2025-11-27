import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Tuple

# Path to the JSON store in the user's home directory
STORE_PATH = Path.home() / ".emoji_mood.json"


def _load_store() -> Dict[str, str]:
    """Load the mood store from disk.

    Returns:
        A mapping of ISO date strings (YYYY‑MM‑DD) to emoji strings.
    """
    if not STORE_PATH.exists():
        return {}
    try:
        with STORE_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Corrupted file – start fresh
        return {}


def _save_store(store: Dict[str, str]) -> None:
    """Persist the mood store to disk.

    Args:
        store: Mapping of dates to emojis.
    """
    with STORE_PATH.open("w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)


def _parse_date(date_str: str) -> str:
    """Validate and return an ISO date string.

    Accepts either "today" (or empty) which resolves to the current date,
    or an explicit YYYY‑MM‑DD string.
    """
    if not date_str or date_str.lower() == "today":
        return date.today().isoformat()
    try:
        # Validate format
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_str}") from exc


def add_entry(mood_emoji: str, entry_date: str = "today") -> Tuple[bool, str]:
    """Add or update a mood entry.

    Args:
        mood_emoji: The emoji representing the mood.
        entry_date: ISO date string or "today".

    Returns:
        (created, message) where ``created`` is True if a new entry was added,
        False if an existing entry was overwritten.
    """
    iso_date = _parse_date(entry_date)
    store = _load_store()
    created = iso_date not in store
    store[iso_date] = mood_emoji
    _save_store(store)
    action = "Added" if created else "Updated"
    return created, f"{action} mood for {iso_date}: {mood_emoji}"


def summary() -> Dict[str, int]:
    """Return a count of each emoji in the store.

    Returns:
        Mapping of emoji to occurrence count.
    """
    store = _load_store()
    counts: Dict[str, int] = {}
    for emoji in store.values():
        counts[emoji] = counts.get(emoji, 0) + 1
    return counts


def _cmd_add(args: argparse.Namespace) -> None:
    _, msg = add_entry(args.emoji, args.date)
    print(msg)


def _cmd_summary(_: argparse.Namespace) -> None:
    counts = summary()
    if not counts:
        print("No mood entries recorded yet.")
        return
    for emoji, cnt in sorted(counts.items(), key=lambda i: i[1], reverse=True):
        print(f"{emoji}: {cnt}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="mood_tracker", description="Log and summarize emoji moods.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add command
    add_parser = subparsers.add_parser("add", help="Add or update a mood entry.")
    add_parser.add_argument("emoji", help="Emoji representing the mood.")
    add_parser.add_argument("date", nargs="?", default="today", help="Date (YYYY-MM-DD) or 'today'.")
    add_parser.set_defaults(func=_cmd_add)

    # summary command
    sum_parser = subparsers.add_parser("summary", help="Show a summary of mood counts.")
    sum_parser.set_defaults(func=_cmd_summary)

    args = parser.parse_args(argv)
    try:
        args.func(args)
    except Exception as e:  # pragma: no cover – defensive
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
