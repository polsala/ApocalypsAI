import argparse
from datetime import datetime
from pathlib import Path
import sys

class ChronicleKeeper:
    """
    Manages the logging and viewing of chronicle entries.
    """
    def __init__(self, log_file: Path = Path("chronicle.log")):
        self.log_file = log_file

    def add_entry(self, entry_text: str) -> None:
        """
        Adds a new timestamped entry to the chronicle log.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_entry = f"[{timestamp}] {entry_text}\n"
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(formatted_entry)
            print(f"Chronicle added: '{entry_text[:50]}...'" if len(entry_text) > 50 else f"Chronicle added: '{entry_text}'")
        except IOError as e:
            print(f"Error writing to chronicle log: {e}", file=sys.stderr)
            sys.exit(1)

    def view_entries(self) -> None:
        """
        Displays all entries from the chronicle log.
        """
        if not self.log_file.exists():
            print("No chronicles found yet. Start by adding an entry!")
            return

        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    print("Chronicle log is empty. Time to make some history!")
                else:
                    print("\n--- Your Chronicles ---\n")
                    print(content.strip())
                    print("\n-----------------------\n")
        except IOError as e:
            print(f"Error reading chronicle log: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Chronicle Keeper: Log your wasteland adventures."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new chronicle entry.")
    add_parser.add_argument("entry_text", type=str, help="The text of your chronicle entry.")

    # View command
    view_parser = subparsers.add_parser("view", help="View all existing chronicle entries.")

    args = parser.parse_args()

    # The log file will be created in the same directory as the script.
    keeper = ChronicleKeeper(log_file=Path(__file__).parent / "chronicle.log")

    if args.command == "add":
        keeper.add_entry(args.entry_text)
    elif args.command == "view":
        keeper.view_entries()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
