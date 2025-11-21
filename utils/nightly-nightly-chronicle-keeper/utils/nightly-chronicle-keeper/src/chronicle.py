import argparse
import datetime
import os

class ChronicleManager:
    CHRONICLE_FILE = ".chronicle.log"

    def _get_chronicle_path(self):
        """Returns the path to the chronicle file."""
        # For self-containment and ease of testing, store in current working directory.
        return os.path.join(os.getcwd(), self.CHRONICLE_FILE)

    def init_chronicle(self):
        """Initializes the chronicle file if it doesn't exist."""
        chronicle_path = self._get_chronicle_path()
        if not os.path.exists(chronicle_path):
            with open(chronicle_path, 'w', encoding='utf-8') as f:
                f.write("") # Create an empty file
            print(f"Chronicle initialized at {chronicle_path}")
        else:
            print(f"Chronicle already exists at {chronicle_path}")

    def add_entry(self, entry_text: str):
        """Adds a new timestamped entry to the chronicle."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {entry_text}"
        chronicle_path = self._get_chronicle_path()
        
        # Ensure the file exists before appending
        if not os.path.exists(chronicle_path):
            self.init_chronicle()

        with open(chronicle_path, 'a', encoding='utf-8') as f:
            f.write(entry + "\n")
        print(f"Entry added: {entry}")

    def _read_all_entries(self) -> list[str]:
        """Reads all entries from the chronicle file."""
        chronicle_path = self._get_chronicle_path()
        if not os.path.exists(chronicle_path):
            return []
        with open(chronicle_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    def list_entries(self, count: int = 10, all_entries: bool = False) -> list[str]:
        """Lists the most recent entries or all entries, printing them to stdout."""
        entries = self._read_all_entries()
        
        if all_entries:
            display_entries = entries
        else:
            display_entries = entries[-count:]
        
        if display_entries:
            for entry in display_entries:
                print(entry)
        else:
            print("No entries found in the chronicle.")

        return display_entries

    def search_entries(self, keyword: str) -> list[str]:
        """Searches entries for a given keyword (case-insensitive), printing results to stdout."""
        entries = self._read_all_entries()
        results = [entry for entry in entries if keyword.lower() in entry.lower()]
        if results:
            for result in results:
                print(result)
        else:
            print(f"No entries found containing '{keyword}'.")
        return results

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Chronicle Keeper: Log and search daily entries."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize the chronicle file.')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new entry to the chronicle.')
    add_parser.add_argument('entry_text', type=str, help='The text of the entry to add.')

    # List command
    list_parser = subparsers.add_parser('list', help='List chronicle entries.')
    list_group = list_parser.add_mutually_exclusive_group()
    list_group.add_argument('--count', type=int, default=10, help='Number of recent entries to list (default: 10).')
    list_group.add_argument('--all', action='store_true', help='List all entries.')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search chronicle entries by keyword.')
    search_parser.add_argument('keyword', type=str, help='The keyword to search for.')

    args = parser.parse_args()
    manager = ChronicleManager()

    if args.command == 'init':
        manager.init_chronicle()
    elif args.command == 'add':
        manager.add_entry(args.entry_text)
    elif args.command == 'list':
        manager.list_entries(count=args.count, all_entries=args.all)
    elif args.command == 'search':
        manager.search_entries(args.keyword)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
