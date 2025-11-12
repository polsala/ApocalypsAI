#!/usr/bin/env python3
"""emoji-mood – a tiny CLI to log daily moods with emojis.

The utility stores entries in a JSON file (default: ~/.emoji_mood_log.json).
It provides two sub‑commands:

* ``add`` – record today’s mood.
* ``stats`` – print a simple frequency table.
"""

import argparse
import datetime
import json
import sys
from pathlib import Path

# Default location for the mood log – user‑writable and hidden.
DEFAULT_DB = Path.home() / ".emoji_mood_log.json"


def load_db(path: Path = DEFAULT_DB) -> dict:
    """Load the JSON database.

    Returns an empty dict if the file does not exist or is malformed.
    """
    if path.is_file():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            # Mock rationale: defensive fallback for corrupted files.
            return {}
    return {}


def save_db(data: dict, path: Path = DEFAULT_DB) -> None:
    """Write *data* to *path* as pretty‑printed JSON."""
    path.write_text(json.dumps(data, indent=2, sort_keys=True))


def add_entry(mood: str, note: str, path: Path = DEFAULT_DB) -> None:
    """Add a mood entry for today.

    * ``mood`` – an emoji string (e.g. "😊").
    * ``note`` – optional short text.
    """
    db = load_db(path)
    today = datetime.date.today().isoformat()
    db[today] = {"mood": mood, "note": note}
    save_db(db, path)


def show_stats(path: Path = DEFAULT_DB) -> None:
    """Print a frequency table of recorded moods."""
    db = load_db(path)
    if not db:
        print("No entries yet.")
        return
    counts: dict[str, int] = {}
    for entry in db.values():
        mood = entry["mood"]
        counts[mood] = counts.get(mood, 0) + 1
    total = sum(counts.values())
    for mood, cnt in sorted(counts.items(), key=lambda i: -i[1]):
        pct = cnt / total * 100
        print(f"{mood}: {cnt} ({pct:.1f}%)")
    print(f"Total days logged: {total}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="emoji-mood",
        description="Log your daily mood with an emoji and view simple stats."
    )
    sub = parser.add_subparsers(dest="cmd")

    # ``add`` sub‑command
    add = sub.add_parser("add", help="Add today's mood")
    add.add_argument("mood", help="Emoji representing your mood, e.g., 😊")
    add.add_argument("-n", "--note", default="", help="Optional short note")
    add.add_argument(
        "-f",
        "--file",
        type=Path,
        default=DEFAULT_DB,
        help="Path to the JSON DB (default: %(default)s)"
    )

    # ``stats`` sub‑command
    stats = sub.add_parser("stats", help="Show mood statistics")
    stats.add_argument(
        "-f",
        "--file",
        type=Path,
        default=DEFAULT_DB,
        help="Path to the JSON DB (default: %(default)s)"
    )

    args = parser.parse_args()
    if args.cmd == "add":
        add_entry(args.mood, args.note, args.file)
        print(f"Logged mood {args.mood} for today.")
    elif args.cmd == "stats":
        show_stats(args.file)
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
