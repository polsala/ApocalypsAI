import argparse
import datetime
import os

LOG_FILE = 'chronicle.log'

def add_entry(message: str):
    """Appends a timestamped message to the log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(entry)
        print(f"Entry added to {LOG_FILE}.")
    except IOError as e:
        print(f"Error writing to log file: {e}")

def view_entries():
    """Reads and prints all entries from the log file."""
    if not os.path.exists(LOG_FILE):
        print(f"No chronicle found at {LOG_FILE}. Start by adding an entry!")
        return

    try:
        with open(LOG_FILE, 'r') as f:
            content = f.read()
            if not content:
                print(f"The chronicle at {LOG_FILE} is empty.")
            else:
                print(content.strip())
    except IOError as e:
        print(f"Error reading log file: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="A simple command-line logbook for your daily chronicle."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new entry to the chronicle')
    add_parser.add_argument('message', type=str, help='The message for your log entry')

    # View command
    view_parser = subparsers.add_parser('view', help='View all entries in the chronicle')

    args = parser.parse_args()

    if args.command == 'add':
        add_entry(args.message)
    elif args.command == 'view':
        view_entries()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
