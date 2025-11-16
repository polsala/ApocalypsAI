import argparse
import datetime
import os

JOURNAL_DIR = "data"
JOURNAL_FILE = os.path.join(JOURNAL_DIR, "journal.txt")

def _get_journal_path():
    """Returns the absolute path to the journal file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir) # Go up from src/ to gloom-gazer-gratitude-journal/
    return os.path.join(base_dir, JOURNAL_FILE)

def _ensure_journal_dir_exists():
    """Ensures the data directory for the journal file exists."""
    journal_path = _get_journal_path()
    journal_dir = os.path.dirname(journal_path)
    os.makedirs(journal_dir, exist_ok=True)

def add_entry(entry_text: str):
    """Adds a new gratitude entry with a timestamp."""
    _ensure_journal_dir_exists()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(_get_journal_path(), "a") as f:
        f.write(f"[{timestamp}] - {entry_text}\n")
    print(f"Entry added: '{entry_text}'")

def get_entries(date_filter: str = None):
    """Retrieves all journal entries, optionally filtered by date."""
    journal_path = _get_journal_path()
    if not os.path.exists(journal_path):
        print("No entries found yet. Start by adding one!")
        return []

    entries = []
    with open(journal_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(line)

    if date_filter:
        filtered_entries = [
            entry for entry in entries
            if entry.startswith(f"[{date_filter}")
        ]
        return filtered_entries
    return entries

def main():
    parser = argparse.ArgumentParser(
        description="Gloom-Gazer's Gratitude Journal: Log and review your grateful thoughts."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new gratitude entry")
    add_parser.add_argument("text", type=str, help="The gratitude entry text")

    # View command
    view_parser = subparsers.add_parser("view", help="View journal entries")
    view_parser.add_argument(
        "--date",
        type=str,
        help="Filter entries by a specific date (YYYY-MM-DD)",
        metavar="YYYY-MM-DD"
    )

    args = parser.parse_args()

    if args.command == "add":
        add_entry(args.text)
    elif args.command == "view":
        entries = get_entries(args.date)
        if entries:
            print("\n--- Gloom-Gazer's Journal Entries ---")
            for entry in entries:
                print(entry)
            print("-------------------------------------\n")
        elif args.date:
            print(f"No entries found for {args.date}.")
        else:
            print("No entries found yet. Start by adding one!")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
