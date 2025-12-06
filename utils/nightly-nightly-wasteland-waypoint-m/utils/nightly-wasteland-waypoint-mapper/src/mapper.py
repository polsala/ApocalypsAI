import argparse
import json
import os

class WaypointManager:
    """Manages the storage and retrieval of wasteland waypoints."""

    def __init__(self, data_file="waypoints.json"):
        self.data_file = data_file
        self.waypoints = self._load_waypoints()

    def _load_waypoints(self):
        """Loads waypoints from the JSON data file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    # Handle empty or malformed JSON files by returning an empty list
                    return []
        return []

    def _save_waypoints(self):
        """Saves the current list of waypoints to the JSON data file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.waypoints, f, indent=4)

    def add_waypoint(self, name, coords, description):
        """Adds a new waypoint. Returns (success, message)."""
        if any(wp['name'].lower() == name.lower() for wp in self.waypoints):
            return False, f"Waypoint '{name}' already exists."
        self.waypoints.append({
            "name": name,
            "coords": coords,
            "description": description
        })
        self._save_waypoints()
        return True, f"Waypoint '{name}' added."

    def list_waypoints(self):
        """Returns a list of all stored waypoints."""
        return self.waypoints

    def find_waypoint(self, name):
        """Finds a waypoint by name (case-insensitive). Returns the waypoint dict or None."""
        for wp in self.waypoints:
            if wp['name'].lower() == name.lower():
                return wp
        return None

    def delete_waypoint(self, name):
        """Deletes a waypoint by name (case-insensitive). Returns (success, message)."""
        initial_len = len(self.waypoints)
        self.waypoints = [wp for wp in self.waypoints if wp['name'].lower() != name.lower()]
        if len(self.waypoints) < initial_len:
            self._save_waypoints()
            return True, f"Waypoint '{name}' deleted."
        return False, f"Waypoint '{name}' not found."

def main():
    """Main function to parse arguments and execute commands."""
    parser = argparse.ArgumentParser(
        description="Manage your wasteland waypoints."
    )
    parser.add_argument("--data-file", default="waypoints.json",
                        help="Specify the JSON file to store waypoints (default: waypoints.json).")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new waypoint.")
    add_parser.add_argument("name", help="Name of the waypoint.")
    add_parser.add_argument("coords", help="Coordinates (e.g., 'N34.05,W118.25').")
    add_parser.add_argument("description", help="Description of the waypoint.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all waypoints.")

    # Find command
    find_parser = subparsers.add_parser("find", help="Find a waypoint by name.")
    find_parser.add_argument("name", help="Name of the waypoint to find.")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a waypoint by name.")
    delete_parser.add_argument("name", help="Name of the waypoint to delete.")

    args = parser.parse_args()

    manager = WaypointManager(args.data_file)

    if args.command == "add":
        success, message = manager.add_waypoint(args.name, args.coords, args.description)
        print(message)
    elif args.command == "list":
        waypoints = manager.list_waypoints()
        if waypoints:
            print("--- Wasteland Waypoints ---")
            for wp in waypoints:
                print(f"Name: {wp['name']}")
                print(f"Coords: {wp['coords']}")
                print(f"Description: {wp['description']}")
                print("-" * 25)
        else:
            print("No waypoints recorded yet. Add some!")
    elif args.command == "find":
        waypoint = manager.find_waypoint(args.name)
        if waypoint:
            print(f"--- Waypoint Found: {waypoint['name']} ---")
            print(f"Coords: {waypoint['coords']}")
            print(f"Description: {waypoint['description']}")
        else:
            print(f"Waypoint '{args.name}' not found.")
    elif args.command == "delete":
        success, message = manager.delete_waypoint(args.name)
        print(message)
    else:
        parser.print_help() # No command given or unknown command

if __name__ == "__main__":
    main()
