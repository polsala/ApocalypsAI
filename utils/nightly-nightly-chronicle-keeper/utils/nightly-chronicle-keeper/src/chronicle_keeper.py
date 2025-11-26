import argparse
import datetime
import os

LOG_FILE_NAME = 'chronicle.log'

def _get_log_path():
    """Returns the absolute path to the log file."""
    # Ensure the log file is created in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, LOG_FILE_NAME)

def add_entry(message: str, tags: list = None):
    """
    Adds a new timestamped entry to the chronicle log file.
    Tags should be provided as a list of strings (e.g., ['#food', '#resource']).
    """
    log_path = _get_log_path()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tag_str = ' '.join(tags) if tags else ''
    entry = f"[{timestamp}] {tag_str} {message.strip()}\n"

    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(entry)
        print(f"Entry added to chronicle: {message}")
    except IOError as e:
        print(f"Error writing to chronicle log: {e}")

def view_entries(tag: str = None):
    """
    Reads and prints entries from the chronicle log file.
    If a tag is provided, only entries containing that tag are printed.
    """
    log_path = _get_log_path()
    if not os.path.exists(log_path):
        print("Chronicle log file not found. Start by adding an entry!")
        return

    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            entries = f.readlines()

        filtered_entries = []
        for entry in entries:
            if tag:
                # Case-insensitive tag matching
                if tag.lower() in entry.lower():
                    filtered_entries.append(entry.strip())
            else:
                filtered_entries.append(entry.strip())

        if filtered_entries:
            for entry in filtered_entries:
                print(entry)
        else:
            if tag:
                print(f"No entries found with tag '{tag}'.")
            else:
                print("No entries found in the chronicle.")

    except IOError as e:
        print(f"Error reading chronicle log: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Chronicle Keeper: Log your post-apocalyptic adventures."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new entry to the chronicle.')
    add_parser.add_argument('message', type=str, help='The message for your chronicle entry.')
    add_parser.add_argument('tags', nargs='*', default=[],
                            help='Optional tags for the entry (e.g., #food #resource).')

    # View command
    view_parser = subparsers.add_parser('view', help='View entries from the chronicle.')
    view_parser.add_argument('tag', nargs='?', type=str,
                             help='Optional tag to filter entries (e.g., #food).')

    args = parser.parse_args()

    if args.command == 'add':
        # Filter out non-tag arguments if any, and ensure tags start with '#'
        tags = [t for t in args.tags if t.startswith('#')]
        add_entry(args.message, tags)
    elif args.command == 'view':
        view_entries(args.tag)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
