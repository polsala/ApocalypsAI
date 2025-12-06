import argparse
import json
import os
from datetime import datetime

DATA_FILE = "catastrophes.json"

def _load_events(filepath):
    # Mock rationale: Avoids actual file system access during tests.
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

def _save_events(filepath, events):
    # Mock rationale: Avoids actual file system access during tests.
    with open(filepath, 'w') as f:
        json.dump(events, f, indent=4)

def add_event(description, filepath=DATA_FILE):
    events = _load_events(filepath)
    timestamp = datetime.now().isoformat()
    events.append({"timestamp": timestamp, "description": description})
    _save_events(filepath, events)
    return f"Event logged: '{description}' at {timestamp}"

def list_events(filepath=DATA_FILE):
    events = _load_events(filepath)
    if not events:
        return "No catastrophic events recorded yet."
    output = ["--- Chronicle of Catastrophes ---"]
    for event in events:
        output.append(f"[{event['timestamp']}] {event['description']}")
    return "\n".join(output)

def search_events(keyword, filepath=DATA_FILE):
    events = _load_events(filepath)
    results = [
        event for event in events
        if keyword.lower() in event['description'].lower()
    ]
    if not results:
        return f"No events found matching '{keyword}'."
    output = [f"--- Search Results for '{keyword}' ---"]
    for event in results:
        output.append(f"[{event['timestamp']}] {event['description']}")
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description="Curate your personal chronicle of catastrophic events."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new catastrophic event.")
    add_parser.add_argument("description", type=str, help="Description of the event.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all recorded events.")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search events by keyword.")
    search_parser.add_argument("keyword", type=str, help="Keyword to search for in event descriptions.")

    args = parser.parse_args()

    if args.command == "add":
        print(add_event(args.description))
    elif args.command == "list":
        print(list_events())
    elif args.command == "search":
        print(search_events(args.keyword))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
