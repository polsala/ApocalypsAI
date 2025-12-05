import json
import os
import sys
from typing import List, Dict, Any, Optional

WAYPOINTS_FILE = "waypoints.json"

class WaypointManager:
    def __init__(self, file_path: str = WAYPOINTS_FILE):
        self.file_path = file_path
        self.waypoints: List[Dict[str, str]] = self._load_waypoints()

    def _load_waypoints(self) -> List[Dict[str, str]]:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {self.file_path} is corrupted. Starting with an empty list.", file=sys.stderr)
                return []
        return []

    def _save_waypoints(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.waypoints, f, indent=2)

    def add_waypoint(self, name: str, description: str, coordinates: Optional[str] = None) -> bool:
        if any(wp['name'].lower() == name.lower() for wp in self.waypoints):
            print(f"Error: Waypoint '{name}' already exists.", file=sys.stderr)
            return False
        
        new_waypoint = {
            "name": name,
            "description": description,
            "coordinates": coordinates if coordinates else "N/A"
        }
        self.waypoints.append(new_waypoint)
        self._save_waypoints()
        return True

    def list_waypoints(self) -> List[Dict[str, str]]:
        return self.waypoints

    def remove_waypoint(self, name: str) -> bool:
        initial_len = len(self.waypoints)
        self.waypoints = [wp for wp in self.waypoints if wp['name'].lower() != name.lower()]
        if len(self.waypoints) < initial_len:
            self._save_waypoints()
            return True
        print(f"Error: Waypoint '{name}' not found.", file=sys.stderr)
        return False

def main():
    manager = WaypointManager()
    args = sys.argv[1:]

    if not args:
        print("Usage:")
        print("  python waypoint_weaver.py add <name> <description> [coordinates]")
        print("  python waypoint_weaver.py list")
        print("  python waypoint_weaver.py remove <name>")
        sys.exit(1)

    command = args[0]

    if command == "add":
        if len(args) < 3:
            print("Usage: python waypoint_weaver.py add <name> <description> [coordinates]", file=sys.stderr)
            sys.exit(1)
        name = args[1]
        description = args[2]
        coordinates = args[3] if len(args) > 3 else None
        if manager.add_waypoint(name, description, coordinates):
            print(f"Waypoint '{name}' added.")
        else:
            sys.exit(1)
    elif command == "list":
        waypoints = manager.list_waypoints()
        if not waypoints:
            print("No waypoints recorded yet.")
        else:
            print("--- Waypoints ---")
            for wp in waypoints:
                print(f"Name: {wp['name']}")
                print(f"  Description: {wp['description']}")
                print(f"  Coordinates: {wp['coordinates']}")
                print("---")
    elif command == "remove":
        if len(args) < 2:
            print("Usage: python waypoint_weaver.py remove <name>", file=sys.stderr)
            sys.exit(1)
        name = args[1]
        if manager.remove_waypoint(name):
            print(f"Waypoint '{name}' removed.")
        else:
            sys.exit(1)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
