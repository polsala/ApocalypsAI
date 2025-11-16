import argparse
import json
import os
import sys
import datetime

# Path to the JSON file that stores moods. Uses the user's home directory.
DATA_PATH = os.path.expanduser("~/.emoji_mood_tracker.json")


def load_data():
    """Load the mood data from the JSON file. Returns an empty dict if the file does not exist."""
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data):
    """Write the mood data to the JSON file, pretty‑printed for readability."""
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def record(mood):
    """Record a mood emoji for today.

    Args:
        mood (str): The emoji representing the user's mood.
    """
    data = load_data()
    today = datetime.date.today().isoformat()
    data.setdefault(today, []).append(mood)
    save_data(data)
    print(f"Recorded mood {mood} for {today}")


def summary():
    """Print a summary of how many times each emoji has been recorded across all days."""
    data = load_data()
    counts = {}
    for moods in data.values():
        for m in moods:
            counts[m] = counts.get(m, 0) + 1
    if not counts:
        print("No moods recorded yet.")
        return
    # Sort by descending count, then alphabetically.
    for mood, cnt in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"{mood}: {cnt}")


def main():
    parser = argparse.ArgumentParser(description="Emoji Mood Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Sub‑command to record a mood.
    rec_parser = subparsers.add_parser("record", help="Record a mood emoji for today")
    rec_parser.add_argument("emoji", help="Emoji representing your mood")

    # Sub‑command to show a summary.
    subparsers.add_parser("summary", help="Show a summary of recorded moods")

    args = parser.parse_args()
    if args.command == "record":
        record(args.emoji)
    elif args.command == "summary":
        summary()
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
