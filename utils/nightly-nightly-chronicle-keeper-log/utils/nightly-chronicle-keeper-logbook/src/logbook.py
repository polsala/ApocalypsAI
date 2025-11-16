import argparse
import datetime
import os

DEFAULT_LOG_FILENAME = 'chronicle.log'

def _get_log_file_path(filename=DEFAULT_LOG_FILENAME):
    """Determines the full path for the log file."""
    # For simplicity, log file is in the current working directory.
    # In a real scenario, one might want a dedicated data directory.
    return os.path.join(os.getcwd(), filename)

def add_entry(message: str, log_file_path: str):
    """Adds a timestamped entry to the log file."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{timestamp}] {message}\n"
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(entry)
        print(f"Entry added to {log_file_path}")
    except IOError as e:
        print(f"Error writing to log file: {e}")

def view_entries(log_file_path: str):
    """Reads and prints all entries from the log file."""
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if content:
                print("\n--- Chronicle Logbook ---")
                print(content.strip())
                print("-------------------------")
            else:
                print(f"Log file {log_file_path} is empty.")
    except FileNotFoundError:
        print(f"Log file {log_file_path} not found. No entries yet.")
    except IOError as e:
        print(f"Error reading log file: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Chronicle Keeper Logbook: Document your apocalypse journey."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new entry to the logbook')
    add_parser.add_argument('message', type=str, help='The message to log')

    # View command
    view_parser = subparsers.add_parser('view', help='View all entries in the logbook')

    args = parser.parse_args()

    log_file = _get_log_file_path()

    if args.command == 'add':
        add_entry(args.message, log_file)
    elif args.command == 'view':
        view_entries(log_file)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
