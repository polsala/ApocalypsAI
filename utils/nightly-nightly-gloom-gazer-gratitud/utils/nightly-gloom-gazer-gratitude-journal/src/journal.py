import argparse
import datetime
import os

LOG_FILE = 'gratitude_log.txt'

def _get_log_path():
    """Returns the absolute path to the log file."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the log file in the same directory
    return os.path.join(script_dir, LOG_FILE)

def add_entry(entry_text: str, log_file_path: str = None):
    """Adds a new timestamped gratitude entry to the log file."""
    if log_file_path is None:
        log_file_path = _get_log_path()

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{timestamp}] {entry_text}\n"
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(entry)
        print(f"Gratitude logged: '{entry_text}'")
    except IOError as e:
        print(f"Error writing to log file: {e}")

def view_entries(log_file_path: str = None):
    """Reads and prints all gratitude entries from the log file."""
    if log_file_path is None:
        log_file_path = _get_log_path()

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            entries = f.readlines()
            if not entries:
                print("No gratitude entries found yet. Start logging some!")
            else:
                print("\n--- Your Gratitude Log ---")
                for entry in entries:
                    print(entry.strip())
                print("-------------------------")
    except FileNotFoundError:
        print("No gratitude log file found. Start by adding your first entry!")
    except IOError as e:
        print(f"Error reading log file: {e}")

def search_entries(keyword: str, log_file_path: str = None):
    """Searches for entries containing the given keyword (case-insensitive)."""
    if log_file_path is None:
        log_file_path = _get_log_path()

    found_entries = []
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if keyword.lower() in line.lower():
                    found_entries.append(line.strip())

        if not found_entries:
            print(f"No entries found containing '{keyword}'.")
        else:
            print(f"\n--- Search Results for '{keyword}' ---")
            for entry in found_entries:
                print(entry)
            print("-------------------------------------")
    except FileNotFoundError:
        print("No gratitude log file found. Cannot search.")
    except IOError as e:
        print(f"Error reading log file: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="A simple gratitude journal for the post-apocalyptic era."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new gratitude entry')
    add_parser.add_argument('entry', type=str, help='The gratitude entry text')

    # View command
    view_parser = subparsers.add_parser('view', help='View all gratitude entries')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search entries by keyword')
    search_parser.add_argument('keyword', type=str, help='The keyword to search for')

    args = parser.parse_args()

    if args.command == 'add':
        add_entry(args.entry)
    elif args.command == 'view':
        view_entries()
    elif args.command == 'search':
        search_entries(args.keyword)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
