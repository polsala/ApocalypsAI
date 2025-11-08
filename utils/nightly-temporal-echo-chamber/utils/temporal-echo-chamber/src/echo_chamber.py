import argparse
import json
import os
from datetime import datetime, timedelta

# Define the path for the echo chamber data file
# This will be relative to the script's location
DATA_FILE = os.path.join(os.path.dirname(__file__), 'echo_chamber_data.json')

def _load_messages():
    """Loads messages from the data file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Handle corrupted JSON or empty file
        return []

def _save_messages(messages):
    """Saves messages to the data file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(messages, f, indent=2)

def add_message(message_content):
    """Adds a new timestamped message."""
    messages = _load_messages()
    timestamp = datetime.now().isoformat()
    messages.append({'timestamp': timestamp, 'message': message_content})
    _save_messages(messages)
    print(f"Echo recorded: '{message_content}'")

def list_messages():
    """Lists all recorded messages."""
    messages = _load_messages()
    if not messages:
        print("The echo chamber is silent. No messages recorded.")
        return

    print("--- Temporal Echo Chamber Messages ---")
    for msg in messages:
        dt_obj = datetime.fromisoformat(msg['timestamp'])
        print(f"{dt_obj.strftime('%Y-%m-%d %H:%M:%S')} - {msg['message']}")
    print("--------------------------------------")

def recall_messages(days):
    """Recalls messages from the last 'days'."""
    messages = _load_messages()
    if not messages:
        print("The echo chamber is silent. No messages recorded.")
        return

    now = datetime.now()
    cutoff_date = now - timedelta(days=days)
    recalled = []

    for msg in messages:
        dt_obj = datetime.fromisoformat(msg['timestamp'])
        if dt_obj >= cutoff_date:
            recalled.append(msg)

    if not recalled:
        print(f"No echoes found from the last {days} day(s).")
        return

    print(f"--- Echoes from the last {days} day(s) ---")
    for msg in recalled:
        dt_obj = datetime.fromisoformat(msg['timestamp'])
        print(f"{dt_obj.strftime('%Y-%m-%d %H:%M:%S')} - {msg['message']}")
    print("--------------------------------------")

def clear_messages():
    """Clears all messages from the echo chamber."""
    _save_messages([])
    print("All echoes have faded from the chamber.")

def main():
    parser = argparse.ArgumentParser(
        description="Temporal Echo Chamber: Record and recall timestamped messages."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new message.')
    add_parser.add_argument('message', type=str, help='The message to record.')

    # List command
    list_parser = subparsers.add_parser('list', help='List all recorded messages.')

    # Recall command
    recall_parser = subparsers.add_parser('recall', help='Recall messages from the last N days.')
    recall_parser.add_argument('days', type=int, help='Number of past days to recall messages from.')

    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear all messages.')

    args = parser.parse_args()

    if args.command == 'add':
        add_message(args.message)
    elif args.command == 'list':
        list_messages()
    elif args.command == 'recall':
        if args.days < 0:
            print("Error: Number of days cannot be negative.")
            return
        recall_messages(args.days)
    elif args.command == 'clear':
        clear_messages()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
