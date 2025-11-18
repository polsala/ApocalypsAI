import argparse
import json
import os
from datetime import datetime

DATA_FILE = 'morale_data.json'

def _load_data():
    """Loads morale data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Handle empty or malformed JSON file
            return []

def _save_data(data):
    """Saves morale data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_entry(mood: int, note: str = None):
    """Adds a new morale entry."""
    if not 1 <= mood <= 5:
        print("Error: Mood must be an integer between 1 and 5.")
        return

    data = _load_data()
    entry = {
        'timestamp': datetime.now().isoformat(),
        'mood': mood,
        'note': note if note else ''
    }
    data.append(entry)
    _save_data(data)
    print(f"Morale entry added: Mood {mood} at {entry['timestamp']}")

def view_entries():
    """Displays all recorded morale entries."""
    data = _load_data()
    if not data:
        print("No morale entries found. Start by adding one!")
        return

    print("\n--- Morale History ---")
    for entry in data:
        timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        mood_str = '⭐' * entry['mood']
        print(f"[{timestamp}] Mood: {mood_str} ({entry['mood']}/5)")
        if entry['note']:
            print(f"  Note: {entry['note']}")
    print("----------------------\n")

def get_summary():
    """Calculates and displays a summary of morale data."""
    data = _load_data()
    if not data:
        print("No morale entries to summarize.")
        return

    total_mood = 0
    mood_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for entry in data:
        total_mood += entry['mood']
        mood_counts[entry['mood']] += 1

    average_mood = total_mood / len(data)

    print("\n--- Morale Summary ---")
    print(f"Total Entries: {len(data)}")
    print(f"Average Mood: {average_mood:.2f}/5")
    print("Mood Distribution:")
    for mood, count in sorted(mood_counts.items()):
        print(f"  {mood}/5 ({'⭐' * mood}): {count} entries")
    print("----------------------\n")

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Morale Monitor - Track your well-being."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new morale entry.')
    add_parser.add_argument('--mood', type=int, required=True, choices=range(1, 6),
                            help='Your mood score (1=dreadful, 5=exhilarated).')
    add_parser.add_argument('--note', type=str, default=None,
                            help='An optional note about your mood.')

    # View command
    view_parser = subparsers.add_parser('view', help='View all morale entries.')

    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Get a summary of morale data.')

    args = parser.parse_args()

    if args.command == 'add':
        add_entry(args.mood, args.note)
    elif args.command == 'view':
        view_entries()
    elif args.command == 'summary':
        get_summary()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
