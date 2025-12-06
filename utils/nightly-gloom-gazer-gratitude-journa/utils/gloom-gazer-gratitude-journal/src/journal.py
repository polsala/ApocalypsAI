import datetime
import os
import random
import sys

JOURNAL_FILE = "journal.txt"
SILVER_LINING_PROMPTS = [
    "What small comfort did you find today?",
    "Who or what made you smile, even for a moment?",
    "What skill did you use or learn that helped you?",
    "What natural beauty did you notice?",
    "What problem did you overcome, no matter how small?",
    "What simple pleasure did you experience?",
    "What act of kindness did you witness or perform?",
    "What unexpected moment of peace did you encounter?",
    "What did you create or fix today?",
    "What sound brought you a moment of calm?",
]

def _get_journal_path():
    """Returns the absolute path to the journal file."""
    # This ensures the journal.txt is created next to the script,
    # regardless of the current working directory from which the script is run.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, JOURNAL_FILE)

def add_entry(entry_text: str):
    """Adds a new gratitude entry to the journal."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {entry_text}\n"
    try:
        with open(_get_journal_path(), "a") as f:
            f.write(entry)
        print(f"Entry added: '{entry_text}'")
    except IOError as e:
        print(f"Error writing to journal: {e}", file=sys.stderr)
        sys.exit(1)

def view_entries():
    """Displays all entries from the journal."""
    try:
        with open(_get_journal_path(), "r") as f:
            entries = f.readlines()
        if not entries:
            print("Your gratitude journal is empty. Start adding entries!")
        else:
            print("--- Your Gratitude Journal ---")
            for entry in entries:
                print(entry.strip())
            print("-----------------------------")
    except FileNotFoundError:
        print("Your gratitude journal is empty. Start adding entries!")
    except IOError as e:
        print(f"Error reading journal: {e}", file=sys.stderr)
        sys.exit(1)

def get_silver_lining_prompt() -> str:
    """Returns a random silver lining prompt."""
    return random.choice(SILVER_LINING_PROMPTS)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python src/journal.py add \"Your gratitude entry here\"")
        print("  python src/journal.py view")
        print("  python src/journal.py prompt")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: 'add' command requires an entry text.", file=sys.stderr)
            sys.exit(1)
        entry_text = sys.argv[2]
        add_entry(entry_text)
    elif command == "view":
        view_entries()
    elif command == "prompt":
        print("Silver Lining Prompt:")
        print(get_silver_lining_prompt())
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
