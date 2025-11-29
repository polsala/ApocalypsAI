import argparse
import os
from datetime import datetime

CHRONICLE_FILE = "chronicle.log"

def get_chronicle_path():
    """Returns the absolute path to the chronicle file."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), CHRONICLE_FILE)

def init_chronicle():
    """Creates the chronicle file if it doesn't exist."""
    chronicle_path = get_chronicle_path()
    if not os.path.exists(chronicle_path):
        try:
            with open(chronicle_path, 'w') as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Chronicle initialized.\n")
            print(f"Chronicle initialized at: {chronicle_path}")
        except IOError as e:
            print(f"Error initializing chronicle: {e}")
            return False
    else:
        print(f"Chronicle already exists at: {chronicle_path}")
    return True

def add_entry(message: str):
    """Appends a timestamped message to the chronicle."""
    chronicle_path = get_chronicle_path()
    if not os.path.exists(chronicle_path):
        print(f"Chronicle file not found. Please run 'init' first.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    try:
        with open(chronicle_path, 'a') as f:
            f.write(entry)
        print(f"Entry added: {message}")
    except IOError as e:
        print(f"Error adding entry: {e}")

def view_chronicle():
    """Prints the entire content of the chronicle."""
    chronicle_path = get_chronicle_path()
    if not os.path.exists(chronicle_path):
        print(f"Chronicle file not found. Please run 'init' first.")
        return

    try:
        with open(chronicle_path, 'r') as f:
            content = f.read()
            if content:
                print("\n--- Chronicle Entries ---")
                print(content.strip())
                print("-------------------------")
            else:
                print("Chronicle is empty.")
    except IOError as e:
        print(f"Error viewing chronicle: {e}")

def search_chronicle(keyword: str):
    """Searches the chronicle for entries containing the keyword."""
    chronicle_path = get_chronicle_path()
    if not os.path.exists(chronicle_path):
        print(f"Chronicle file not found. Please run 'init' first.")
        return

    found_entries = []
    try:
        with open(chronicle_path, 'r') as f:
            for line in f:
                if keyword.lower() in line.lower():
                    found_entries.append(line.strip())
    except IOError as e:
        print(f"Error searching chronicle: {e}")
        return

    if found_entries:
        print(f"\n--- Search Results for '{keyword}' ---")
        for entry in found_entries:
            print(entry)
        print("------------------------------------")
    else:
        print(f"No entries found containing '{keyword}'.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Chronicle Keeper: Log your daily observations."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initializes the chronicle file.")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new entry to the chronicle.")
    add_parser.add_argument("message", type=str, help="The message to add to the chronicle.")

    # View command
    view_parser = subparsers.add_parser("view", help="View all entries in the chronicle.")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search entries in the chronicle.")
    search_parser.add_argument("keyword", type=str, help="The keyword to search for.")

    args = parser.parse_args()

    if args.command == "init":
        init_chronicle()
    elif args.command == "add":
        add_entry(args.message)
    elif args.command == "view":
        view_chronicle()
    elif args.command == "search":
        search_chronicle(args.keyword)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
