import json
import os
import sys

# Filename for storing waypoints
WAYPOINTS_FILE = 'waypoints.json'

def _load_waypoints():
    """Loads waypoints from the JSON file."""
    if not os.path.exists(WAYPOINTS_FILE):
        return {}
    try:
        with open(WAYPOINTS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {WAYPOINTS_FILE} is corrupted. Starting with an empty tracker.", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Error loading waypoints: {e}", file=sys.stderr)
        return {}

def _save_waypoints(waypoints):
    """Saves waypoints to the JSON file."""
    try:
        with open(WAYPOINTS_FILE, 'w') as f:
            json.dump(waypoints, f, indent=4)
    except Exception as e:
        print(f"Error saving waypoints: {e}", file=sys.stderr)

def add_waypoint(name, latitude, longitude, notes=None):
    """Adds a new waypoint."""
    waypoints = _load_waypoints()
    if name in waypoints:
        print(f"Error: Waypoint '{name}' already exists. Use 'get' to view or 'delete' to remove first.", file=sys.stderr)
        return False
    
    try:
        lat = float(latitude)
        lon = float(longitude)
    except ValueError:
        print("Error: Latitude and Longitude must be valid numbers.", file=sys.stderr)
        return False

    waypoints[name] = {
        'latitude': lat,
        'longitude': lon,
        'notes': notes if notes else "No notes."
    }
    _save_waypoints(waypoints)
    print(f"Waypoint '{name}' added successfully.")
    return True

def list_waypoints():
    """Lists all stored waypoints."""
    waypoints = _load_waypoints()
    if not waypoints:
        print("No waypoints tracked yet. Add some with 'add'!")
        return

    print("--- Tracked Waypoints ---")
    for name, data in waypoints.items():
        notes_snippet = data['notes']
        if len(notes_snippet) > 50:
            notes_snippet = notes_snippet[:47] + "..."
        print(f"  Name: {name}")
        print(f"  Coords: {data['latitude']:.4f}, {data['longitude']:.4f}")
        print(f"  Notes: {notes_snippet}")
        print("-" * 25)

def get_waypoint(name):
    """Retrieves and displays details for a specific waypoint."""
    waypoints = _load_waypoints()
    if name not in waypoints:
        print(f"Error: Waypoint '{name}' not found.", file=sys.stderr)
        return
    
    data = waypoints[name]
    print(f"--- Waypoint Details: {name} ---")
    print(f"  Latitude: {data['latitude']:.6f}")
    print(f"  Longitude: {data['longitude']:.6f}")
    print(f"  Notes: {data['notes']}")
    print("-" * 30)

def delete_waypoint(name):
    """Deletes a waypoint."""
    waypoints = _load_waypoints()
    if name not in waypoints:
        print(f"Error: Waypoint '{name}' not found.", file=sys.stderr)
        return False
    
    del waypoints[name]
    _save_waypoints(waypoints)
    print(f"Waypoint '{name}' deleted successfully.")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python tracker.py <command> [args...]")
        print("Commands: add, list, get, delete")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) < 5:
            print("Usage: python tracker.py add <name> <latitude> <longitude> [notes...]")
            sys.exit(1)
        name = sys.argv[2]
        latitude = sys.argv[3]
        longitude = sys.argv[4]
        notes = " ".join(sys.argv[5:]) if len(sys.argv) > 5 else None
        add_waypoint(name, latitude, longitude, notes)
    elif command == 'list':
        list_waypoints()
    elif command == 'get':
        if len(sys.argv) < 3:
            print("Usage: python tracker.py get <name>")
            sys.exit(1)
        name = sys.argv[2]
        get_waypoint(name)
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Usage: python tracker.py delete <name>")
            sys.exit(1)
        name = sys.argv[2]
        delete_waypoint(name)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
