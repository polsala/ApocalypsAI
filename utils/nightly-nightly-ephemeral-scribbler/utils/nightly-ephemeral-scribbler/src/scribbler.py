import argparse
import os
import sys

DEFAULT_NOTES_FILE = "scribbles.txt"

def get_notes_file_path(file_arg: str | None) -> str:
    """Determines the path to the notes file."""
    return file_arg if file_arg else DEFAULT_NOTES_FILE

def add_note(note_content: str, file_path: str) -> None:
    """Adds a new note to the notes file."""
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(note_content + '\n')
        print(f"Note added: '{note_content}'")
    except IOError as e:
        print(f"Error adding note to '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)

def list_notes(file_path: str) -> None:
    """Lists all notes from the notes file."""
    if not os.path.exists(file_path):
        print("No notes found yet. Start scribbling!")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            notes = f.readlines()
        if not notes:
            print("No notes found yet. Start scribbling!")
            return

        print("--- Your Ephemeral Scribbles ---")
        for i, note in enumerate(notes, 1):
            print(f"{i}. {note.strip()}")
        print("-------------------------------")
    except IOError as e:
        print(f"Error listing notes from '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)

def clear_notes(file_path: str) -> None:
    """Clears all notes from the notes file."""
    if not os.path.exists(file_path):
        print("No notes file to clear.")
        return

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.truncate(0) # Clear the file content
        print(f"All notes cleared from '{file_path}'.")
    except IOError as e:
        print(f"Error clearing notes from '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="A whimsical utility for quickly jotting down, listing, and clearing temporary notes."
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        default=DEFAULT_NOTES_FILE,
        help=f"Specify the notes file path (default: {DEFAULT_NOTES_FILE})"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new note")
    add_parser.add_argument("note", type=str, help="The content of the note to add")

    # List command
    list_parser = subparsers.add_parser("list", help="List all notes")

    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear all notes")

    args = parser.parse_args()

    notes_file = get_notes_file_path(args.file)

    if args.command == "add":
        add_note(args.note, notes_file)
    elif args.command == "list":
        list_notes(notes_file)
    elif args.command == "clear":
        clear_notes(notes_file)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
