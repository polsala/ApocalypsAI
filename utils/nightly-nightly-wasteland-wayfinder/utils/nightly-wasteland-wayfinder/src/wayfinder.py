import json
import os
import sys

DATA_FILE = 'landmarks.json'

def _load_landmarks():
    """Loads landmarks from the JSON data file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return [] # Return empty list if file is corrupt

def _save_landmarks(landmarks):
    """Saves landmarks to the JSON data file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(landmarks, f, indent=4)

def add_landmark(name, coords, type, description=None):
    """Adds a new landmark."""
    landmarks = _load_landmarks()
    if any(l['name'].lower() == name.lower() for l in landmarks):
        print(f"Error: Landmark '{name}' already exists.")
        return False

    new_landmark = {
        'name': name,
        'coords': coords,
        'type': type,
        'description': description
    }
    landmarks.append(new_landmark)
    _save_landmarks(landmarks)
    print(f"Landmark '{name}' added successfully.")
    return True

def list_landmarks():
    """Lists all stored landmarks."""
    landmarks = _load_landmarks()
    if not landmarks:
        print("No landmarks recorded yet.")
        return

    print("\n--- Recorded Landmarks ---")
    for i, landmark in enumerate(landmarks):
        desc = f" ({landmark['description']})" if landmark['description'] else ""
        print(f"{i+1}. Name: {landmark['name']}")
        print(f"   Coords: {landmark['coords']}")
        print(f"   Type: {landmark['type']}{desc}")
        print("-" * 25)
    print("--------------------------\n")

def find_landmarks(query):
    """Finds landmarks matching a query by name or type."""
    landmarks = _load_landmarks()
    found = [
        l for l in landmarks
        if query.lower() in l['name'].lower() or query.lower() == l['type'].lower()
    ]

    if not found:
        print(f"No landmarks found matching '{query}'.")
        return

    print(f"\n--- Landmarks matching '{query}' ---")
    for i, landmark in enumerate(found):
        desc = f" ({landmark['description']})" if landmark['description'] else ""
        print(f"{i+1}. Name: {landmark['name']}")
        print(f"   Coords: {landmark['coords']}")
        print(f"   Type: {landmark['type']}{desc}")
        print("-" * 25)
    print("-------------------------------------\n")

def remove_landmark(name):
    """Removes a landmark by name."""
    landmarks = _load_landmarks()
    initial_count = len(landmarks)
    landmarks = [l for l in landmarks if l['name'].lower() != name.lower()]

    if len(landmarks) == initial_count:
        print(f"Error: Landmark '{name}' not found.")
        return False

    _save_landmarks(landmarks)
    print(f"Landmark '{name}' removed successfully.")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python wayfinder.py <command> [arguments]")
        print("Commands:")
        print("  add <name> <coords> <type> [description]")
        print("  list")
        print("  find <query>")
        print("  remove <name>")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) < 5:
            print("Usage: python wayfinder.py add <name> <coords> <type> [description]")
            sys.exit(1)
        name, coords, type_ = sys.argv[2], sys.argv[3], sys.argv[4]
        description = sys.argv[5] if len(sys.argv) > 5 else None
        add_landmark(name, coords, type_, description)
    elif command == 'list':
        list_landmarks()
    elif command == 'find':
        if len(sys.argv) < 3:
            print("Usage: python wayfinder.py find <query>")
            sys.exit(1)
        query = sys.argv[2]
        find_landmarks(query)
    elif command == 'remove':
        if len(sys.argv) < 3:
            print("Usage: python wayfinder.py remove <name>")
            sys.exit(1)
        name = sys.argv[2]
        remove_landmark(name)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
