import argparse
import datetime
import os
from pathlib import Path

# Define file paths relative to the script's directory
# When run as `python src/chronicle.py` from `utils/chronicle-keeper/`, SCRIPT_DIR is `src/`
# So, LOG_FILE and CONFIG_FILE are in the parent directory, i.e., `utils/chronicle-keeper/`
SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR.parent / 'chronicle.log'
CONFIG_FILE = SCRIPT_DIR.parent / 'chronicle.config'

DEFAULT_DOOM_DATE = datetime.date(2999, 12, 31) # A far-future default

def _get_doom_date() -> datetime.date:
    """Reads the doom date from the config file, or returns a default."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                date_str = f.read().strip()
                if date_str:
                    return datetime.date.fromisoformat(date_str)
        except (ValueError, IOError):
            pass # Fallback to default if file is corrupt or unreadable
    return DEFAULT_DOOM_DATE

def _save_doom_date(date_obj: datetime.date):
    """Saves the doom date to the config file."""
    with open(CONFIG_FILE, 'w') as f:
        f.write(date_obj.isoformat())

def add_entry(message: str):
    """Adds a new timestamped entry to the chronicle log."""
    now = datetime.datetime.now()
    doom_date = _get_doom_date()
    
    category = "PRE-APOCALYPSE" if now.date() < doom_date else "POST-APOCALYPSE"
    
    entry = f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] [{category}] {message}"
    
    with open(LOG_FILE, 'a') as f:
        f.write(entry + '\n')
    print(f"Entry added: {entry}")

def list_entries(category_filter: str = None):
    """Lists all entries, optionally filtered by category."""
    if not LOG_FILE.exists():
        print("No chronicle entries found. Start by adding one!")
        return

    print("\n--- Chronicle Entries ---")
    with open(LOG_FILE, 'r') as f:
        for line in f:
            if category_filter:
                if category_filter.upper() == 'PRE' and '[PRE-APOCALYPSE]' in line:
                    print(line.strip())
                elif category_filter.upper() == 'POST' and '[POST-APOCALYPSE]' in line:
                    print(line.strip())
            else:
                print(line.strip())
    print("-------------------------")

def config_doom_date(date_str: str = None):
    """Sets or displays the Doom Date."""
    if date_str:
        try:
            new_doom_date = datetime.date.fromisoformat(date_str)
            _save_doom_date(new_doom_date)
            print(f"Doom Date set to: {new_doom_date.isoformat()}")
        except ValueError:
            print(f"Error: Invalid date format. Please use YYYY-MM-DD (e.g., 2025-12-31).")
    else:
        current_doom_date = _get_doom_date()
        print(f"Current Doom Date: {current_doom_date.isoformat()}")

def main():
    parser = argparse.ArgumentParser(
        description="Chronicle Keeper: Your Personal Apocalyptic Journal."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new journal entry.')
    add_parser.add_argument('message', type=str, help='The content of the journal entry.')

    # List command
    list_parser = subparsers.add_parser('list', help='List all entries, or filter by category.')
    list_parser.add_argument('category', type=str, nargs='?', choices=['pre', 'post'],
                              help='Filter entries by category (pre or post).')

    # Config command
    config_parser = subparsers.add_parser('config', help='Set or view the Doom Date.')
    config_parser.add_argument('date', type=str, nargs='?',
                                help='The new Doom Date in YYYY-MM-DD format (e.g., 2025-12-31).')

    args = parser.parse_args()

    if args.command == 'add':
        add_entry(args.message)
    elif args.command == 'list':
        list_entries(args.category)
    elif args.command == 'config':
        config_doom_date(args.date)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
