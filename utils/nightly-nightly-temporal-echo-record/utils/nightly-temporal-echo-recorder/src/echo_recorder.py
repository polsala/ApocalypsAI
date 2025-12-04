import json
import os
import sys
from datetime import datetime, timedelta

ECHOES_FILE = os.path.join(os.path.dirname(__file__), 'echoes.json')
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

def _load_echoes():
    """Loads echoes from the JSON file."""
    if not os.path.exists(ECHOES_FILE):
        return []
    try:
        with open(ECHOES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Handle corrupted or empty JSON file gracefully
        return []

def _save_echoes(echoes):
    """Saves echoes to the JSON file."""
    with open(ECHOES_FILE, 'w', encoding='utf-8') as f:
        json.dump(echoes, f, indent=2, ensure_ascii=False)

def add_echo(message):
    """Adds a new echo with the current timestamp."""
    echoes = _load_echoes()
    timestamp = datetime.now().strftime(DATE_FORMAT)
    echoes.append({"timestamp": timestamp, "message": message})
    _save_echoes(echoes)
    print(f"Echo recorded: '{message}' at {timestamp}")

def list_echoes():
    """Lists all recorded echoes, ordered by recency."""
    echoes = _load_echoes()
    if not echoes:
        print("The temporal void is silent. No echoes found.")
        return

    # Sort by timestamp in descending order (most recent first)
    sorted_echoes = sorted(echoes, key=lambda x: x['timestamp'], reverse=True)

    print("Whispers from the Temporal Void:")
    for i, echo in enumerate(sorted_echoes):
        print(f"  [{i+1}] {echo['timestamp']} - {echo['message']}")

def search_echoes(keyword):
    """Searches echoes for a given keyword (case-insensitive)."""
    echoes = _load_echoes()
    if not echoes:
        print("The temporal void is silent. No echoes to search.")
        return

    found_echoes = [
        echo for echo in echoes
        if keyword.lower() in echo['message'].lower()
    ]

    if not found_echoes:
        print(f"No echoes containing '{keyword}' found in the temporal void.")
        return

    print(f"Echoes containing '{keyword}':")
    for i, echo in enumerate(found_echoes):
        print(f"  [{i+1}] {echo['timestamp']} - {echo['message']}")

def purge_old_echoes(days):
    """Removes echoes older than a specified number of days."""
    echoes = _load_echoes()
    if not echoes:
        print("The temporal void is already clean. No echoes to purge.")
        return

    cutoff_date = datetime.now() - timedelta(days=days)
    
    new_echoes = []
    purged_count = 0
    for echo in echoes:
        try:
            echo_timestamp = datetime.strptime(echo['timestamp'], DATE_FORMAT)
            if echo_timestamp >= cutoff_date:
                new_echoes.append(echo)
            else:
                purged_count += 1
        except ValueError:
            # Malformed timestamp, keep it to avoid data loss, but log if this were a production system.
            new_echoes.append(echo)

    if purged_count > 0:
        _save_echoes(new_echoes)
        print(f"Purged {purged_count} echoes older than {days} days from the temporal void.")
    else:
        print(f"No echoes older than {days} days found to purge.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/echo_recorder.py <command> [args]")
        print("Commands: add <message>, list, search <keyword>, purge <days>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: python src/echo_recorder.py add <message>")
            sys.exit(1)
        message = " ".join(sys.argv[2:])
        add_echo(message)
    elif command == "list":
        list_echoes()
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: python src/echo_recorder.py search <keyword>")
            sys.exit(1)
        keyword = sys.argv[2]
        search_echoes(keyword)
    elif command == "purge":
        if len(sys.argv) < 3:
            print("Usage: python src/echo_recorder.py purge <days>")
            sys.exit(1)
        try:
            days = int(sys.argv[2])
            if days < 0:
                raise ValueError # Negative days are not sensible for purging old items
            purge_old_echoes(days)
        except ValueError:
            print("Error: 'days' must be a non-negative integer.")
            sys.exit(1)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
