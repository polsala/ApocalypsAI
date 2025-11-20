import argparse
import datetime
import json
import sys
from pathlib import Path

# Path to the JSON file that stores moods (next to this script)
DATA_FILE = Path(__file__).with_name("mood_data.json")


def _load_json(path: Path) -> dict:
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_json(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class MoodTracker:
    """Simple emoji‑based mood logger.

    The data format is a mapping of ISO‑date strings to a single emoji.
    """

    def __init__(self, data_path: Path = DATA_FILE):
        self._data_path = Path(data_path)
        self._data = _load_json(self._data_path)

    def add_mood(self, date: str, emoji: str) -> None:
        """Record *emoji* for the given ISO *date* string.
        Overwrites any existing entry for that date.
        """
        self._data[date] = emoji
        _save_json(self._data_path, self._data)

    def get_summary(self) -> dict:
        """Return a dict mapping each emoji to the number of occurrences.
        """
        summary: dict[str, int] = {}
        for e in self._data.values():
            summary[e] = summary.get(e, 0) + 1
        return summary

    # Internal helpers for CLI convenience
    def _today_iso(self) -> str:
        return datetime.date.today().isoformat()

    def cli_add(self, emoji: str) -> None:
        today = self._today_iso()
        self.add_mood(today, emoji)
        print(f"Recorded mood {emoji} for {today}")

    def cli_summary(self) -> None:
        summary = self.get_summary()
        if not summary:
            print("No moods recorded yet.")
            return
        for emoji, count in sorted(summary.items(), key=lambda i: -i[1]):
            print(f"{emoji}: {count}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Emoji Mood Tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add today's mood")
    add.add_argument("emoji", help="Emoji representing your mood")

    sub.add_parser("summary", help="Show aggregated mood counts")
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    tracker = MoodTracker()

    if args.command == "add":
        tracker.cli_add(args.emoji)
    elif args.command == "summary":
        tracker.cli_summary()
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
