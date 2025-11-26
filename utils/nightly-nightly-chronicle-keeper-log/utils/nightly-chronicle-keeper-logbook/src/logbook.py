import argparse
import os
from datetime import datetime

class ChronicleKeeper:
    def __init__(self, log_file_path="logbook.txt"):
        self.log_file_path = log_file_path

    def _get_log_file_path(self):
        # Ensure the log file is created in the same directory as the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, self.log_file_path)

    def add_entry(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}\n"
        try:
            with open(self._get_log_file_path(), "a", encoding="utf-8") as f:
                f.write(entry)
            print(f"Entry added: {message}")
        except IOError as e:
            print(f"Error writing to log file: {e}")

    def list_entries(self):
        try:
            with open(self._get_log_file_path(), "r", encoding="utf-8") as f:
                entries = f.readlines()
            if not entries:
                print("No entries found in the chronicle.")
                return

            print("--- Chronicle Entries ---")
            for entry in entries:
                print(entry.strip())
            print("-------------------------")
        except FileNotFoundError:
            print("No chronicle file found. Start by adding an entry!")
        except IOError as e:
            print(f"Error reading log file: {e}")

    def search_entries(self, keyword: str):
        found_entries = []
        try:
            with open(self._get_log_file_path(), "r", encoding="utf-8") as f:
                for line in f:
                    if keyword.lower() in line.lower():
                        found_entries.append(line.strip())

            if not found_entries:
                print(f"No entries found containing '{keyword}'.")
                return

            print(f"--- Entries containing '{keyword}' ---")
            for entry in found_entries:
                print(entry)
            print("------------------------------------")
        except FileNotFoundError:
            print("No chronicle file found. Start by adding an entry!")
        except IOError as e:
            print(f"Error reading log file: {e}")

    def clear_entries(self):
        confirm = input("Are you sure you want to clear ALL chronicle entries? This cannot be undone. (yes/no): ").lower()
        if confirm == "yes":
            try:
                with open(self._get_log_file_path(), "w", encoding="utf-8") as f:
                    f.write("") # Truncate the file
                print("All chronicle entries have been cleared.")
            except IOError as e:
                print(f"Error clearing log file: {e}")
        else:
            print("Chronicle clearing cancelled.")

def main():
    parser = argparse.ArgumentParser(
        description="A simple command-line utility for creating and managing timestamped log entries."
    )
    parser.add_argument(
        "--log-file",
        default="logbook.txt",
        help="Specify a custom log file name (default: logbook.txt)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new timestamped entry.")
    add_parser.add_argument("message", type=str, help="The message for the log entry.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all chronicle entries.")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search entries by keyword.")
    search_parser.add_argument("keyword", type=str, help="The keyword to search for.")

    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear all chronicle entries.")

    args = parser.parse_args()

    keeper = ChronicleKeeper(log_file_path=args.log_file)

    if args.command == "add":
        keeper.add_entry(args.message)
    elif args.command == "list":
        keeper.list_entries()
    elif args.command == "search":
        keeper.search_entries(args.keyword)
    elif args.command == "clear":
        keeper.clear_entries()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
