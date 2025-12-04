import json
import os
import sys
import argparse
from datetime import datetime, timedelta

# Define the file where notes will be stored
NOTES_FILE = os.path.join(os.path.dirname(__file__), 'chrono_scribble_notes.json')

def _load_notes():
    """Loads notes from the JSON file."""
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Handle corrupted or empty JSON file
        return []

def _save_notes(notes):
    """Saves notes to the JSON file."""
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=2)

def parse_duration(duration_str):
    """Parses a duration string (e.g., '2h', '30m', '1d') into a timedelta object."""
    if not duration_str:
        return timedelta(hours=24) # Default to 24 hours if no duration specified

    unit = duration_str[-1].lower()
    value = int(duration_str[:-1])

    if unit == 's':
        return timedelta(seconds=value)
    elif unit == 'm':
        return timedelta(minutes=value)
    elif unit == 'h':
        return timedelta(hours=value)
    elif unit == 'd':
        return timedelta(days=value)
    elif unit == 'w':
        return timedelta(weeks=value)
    else:
        raise ValueError(f"Invalid duration unit: {unit}. Use s, m, h, d, or w.")

def add_note(content, expires_in_duration=None):
    """Adds a new note with an optional expiry duration."""
    notes = _load_notes()
    now = datetime.now()

    expiry_time = None
    if expires_in_duration:
        expiry_time = now + expires_in_duration
    else:
        # Default expiry if not specified, e.g., 24 hours
        expiry_time = now + timedelta(hours=24)

    note = {
        'id': len(notes) + 1, # Simple ID generation
        'content': content,
        'created_at': now.isoformat(),
        'expires_at': expiry_time.isoformat() if expiry_time else None
    }
    notes.append(note)
    _save_notes(notes)
    print(f"Note added (ID: {note['id']}). Expires at: {note['expires_at'] or 'Never'}")

def list_notes():
    """Lists all active (non-expired) notes."""
    notes = _load_notes()
    now = datetime.now()
    active_notes = []

    for note in notes:
        expires_at_str = note.get('expires_at')
        if expires_at_str:
            expires_at = datetime.fromisoformat(expires_at_str)
            if expires_at > now:
                active_notes.append(note)
        else:
            # Notes without an expiry (shouldn't happen with current add_note logic, but for robustness)
            active_notes.append(note)

    if not active_notes:
        print("No active chrono-scribbles found.")
        return

    print("--- Active Chrono-Scribbles ---")
    for note in active_notes:
        expires_at_dt = datetime.fromisoformat(note['expires_at'])
        time_left = expires_at_dt - now
        print(f"ID: {note['id']}\n  Content: {note['content']}\n  Expires in: {str(time_left).split('.')[0]}\n")
    print("-------------------------------")

def clean_expired_notes():
    """Removes all expired notes from the pad."""
    notes = _load_notes()
    now = datetime.now()
    initial_count = len(notes)
    active_notes = []

    for note in notes:
        expires_at_str = note.get('expires_at')
        if expires_at_str:
            expires_at = datetime.fromisoformat(expires_at_str)
            if expires_at > now:
                active_notes.append(note)
        else:
            active_notes.append(note)

    _save_notes(active_notes)
    removed_count = initial_count - len(active_notes)
    if removed_count > 0:
        print(f"Cleaned up {removed_count} expired chrono-scribbles.")
    else:
        print("No expired chrono-scribbles to clean.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Chrono-Scribble Pad: Your ephemeral memory aid."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new chrono-scribble.')
    add_parser.add_argument('content', type=str, help='The content of the note.')
    add_parser.add_argument(
        '--expires-in', type=str, default=None,
        help='Duration until the note expires (e.g., "2h", "30m", "1d"). Defaults to 24h.'
    )

    # List command
    list_parser = subparsers.add_parser('list', help='List active chrono-scribbles.')

    # Clean command
    clean_parser = subparsers.add_parser('clean', help='Clean up expired chrono-scribbles.')

    args = parser.parse_args()

    if args.command == 'add':
        try:
            duration = parse_duration(args.expires_in)
            add_note(args.content, duration)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.command == 'list':
        list_notes()
    elif args.command == 'clean':
        clean_expired_notes()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
