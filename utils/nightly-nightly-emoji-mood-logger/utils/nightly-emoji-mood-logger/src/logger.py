"""Emoji Mood Logger utility.

Provides functions to select a random mood emoji and log it with a timestamp.
"""

import argparse
import datetime
import random
from pathlib import Path
from typing import List

MOOD_EMOJIS: List[str] = [
    "😀", "😐", "😔", "🤩", "😎", "🤔", "😴", "🤪", "🥳", "😢"
]

def get_mood_emoji() -> str:
    """Return a random mood emoji."""
    return random.choice(MOOD_EMOJIS)

def format_entry(emoji: str, now: datetime.datetime | None = None) -> str:
    """Format the log entry with timestamp and emoji."""
    now = now or datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    return f"{timestamp} - {emoji}"

def log_mood(output_path: Path | str = "mood.log") -> str:
    """Append a mood entry to the given log file.

    Returns the written line for convenience.
    """
    emoji = get_mood_emoji()
    entry = format_entry(emoji)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(entry + "\n")
    return entry

def main() -> None:
    parser = argparse.ArgumentParser(description="Log a random mood emoji with timestamp.")
    parser.add_argument(
        "--output",
        "-o",
        default="mood.log",
        help="Path to the log file (default: mood.log)",
    )
    args = parser.parse_args()
    entry = log_mood(args.output)
    print(entry)

if __name__ == "__main__":
    main()
