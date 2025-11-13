import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Path to the JSON file that stores moods
DATA_PATH = Path.home() / ".emoji_mood_tracker.json"


def load_data():
    """Load the mood dictionary from the JSON file.

    Returns:
        dict: Mapping of ISO date strings to emoji strings.
    """
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data):
    """Write the mood dictionary to the JSON file.

    Args:
        data (dict): Mapping of ISO date strings to emoji strings.
    """
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_entry(date_str, emoji):
    """Add or update a mood entry for a given date.

    Args:
        date_str (str): Date in ISO format (YYYY‑MM‑DD).
        emoji (str): Emoji representing the mood.
    """
    data = load_data()
    data[date_str] = emoji
    save_data(data)


def summary(days):
    """Return a plain‑text summary of moods for the last *days* days.

    Args:
        days (int): Number of days to include, counting back from today.

    Returns:
        str: Multiline string with one line per day.
    """
    data = load_data()
    today = datetime.today()
    start = today - timedelta(days=days - 1)
    lines = []
    for i in range(days):
        day = (start + timedelta(days=i)).date()
        day_str = day.isoformat()
        mood = data.get(day_str, "(no entry)")
        lines.append(f"{day_str}: {mood}")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Commands: add <date> <emoji> | summary <days>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) == 4:
        add_entry(sys.argv[2], sys.argv[3])
        print(f"Added mood for {sys.argv[2]}")
    elif cmd == "summary" and len(sys.argv) == 3:
        try:
            days = int(sys.argv[2])
        except ValueError:
            print("Days must be an integer")
            sys.exit(1)
        print(summary(days))
    else:
        print("Invalid arguments")
        sys.exit(1)


if __name__ == "__main__":
    main()
