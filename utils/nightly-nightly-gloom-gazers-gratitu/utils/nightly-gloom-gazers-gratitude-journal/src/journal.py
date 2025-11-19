import argparse
import datetime
import os

def get_log_directory():
    """Returns the path to the logs directory."""
    # Assumes the script is run from the utility's root or src/
    # Adjust path if script execution context changes
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, '..', 'logs')

def get_log_file_path(date: datetime.date):
    """Returns the path to the log file for a given date."""
    log_dir = get_log_directory()
    os.makedirs(log_dir, exist_ok=True) # Ensure directory exists
    return os.path.join(log_dir, f"{date.strftime('%Y-%m-%d')}.txt")

def add_entry(entry_text: str):
    """Adds a new gratitude entry with a timestamp."""
    now = datetime.datetime.now()
    log_file = get_log_file_path(now.date())
    timestamp = now.strftime('%H:%M:%S')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {entry_text}\n")
    print(f"Gratitude logged for {now.date().strftime('%Y-%m-%d')}.")

def view_entries(date_str: str = None, view_all: bool = False):
    """Views gratitude entries for a specific date or all entries."""
    if view_all:
        log_dir = get_log_directory()
        if not os.path.exists(log_dir):
            print("No gratitude entries found yet.")
            return

        all_entries = []
        for filename in sorted(os.listdir(log_dir)):
            if filename.endswith('.txt'):
                file_path = os.path.join(log_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    all_entries.append(f"\n--- {filename.replace('.txt', '')} ---\n")
                    all_entries.extend(f.readlines())
        
        if not all_entries:
            print("No gratitude entries found yet.")
            return
        
        print("".join(all_entries))
        return

    target_date = datetime.date.today()
    if date_str:
        try:
            target_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print(f"Error: Invalid date format '{date_str}'. Please use YYYY-MM-DD.")
            return

    log_file = get_log_file_path(target_date)
    
    if not os.path.exists(log_file):
        print(f"No gratitude entries found for {target_date.strftime('%Y-%m-%d')}.")
        return

    print(f"\n--- Gratitude for {target_date.strftime('%Y-%m-%d')} ---\n")
    with open(log_file, 'r', encoding='utf-8') as f:
        print(f.read())

def main():
    parser = argparse.ArgumentParser(
        description="Gloom-Gazer's Gratitude Journal: Log your moments of appreciation."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new gratitude entry.')
    add_parser.add_argument('entry', type=str, help='The gratitude entry text.')

    # View command
    view_parser = subparsers.add_parser('view', help='View gratitude entries.')
    view_parser.add_argument(
        'date', type=str, nargs='?',
        help='Optional: Date to view entries (YYYY-MM-DD). Defaults to today.'
    )
    view_parser.add_argument(
        '--all', action='store_true',
        help='View all gratitude entries across all dates.'
    )

    args = parser.parse_args()

    if args.command == 'add':
        add_entry(args.entry)
    elif args.command == 'view':
        view_entries(args.date, args.all)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
