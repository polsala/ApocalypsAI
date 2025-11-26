import argparse
import json
import os
from typing import List, Dict, Optional

class WaypointManager:
    def __init__(self, data_file: str = 'waypoints.json'):
        self.data_file = data_file
        self.waypoints: List[Dict] = []
        self._load_waypoints()

    def _load_waypoints(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.waypoints = json.load(f)
            except json.JSONDecodeError:
                # Handle corrupted or empty JSON file gracefully
                self.waypoints = []
        else:
            self.waypoints = []

    def _save_waypoints(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.waypoints, f, indent=2)

    def add_waypoint(self, name: str, lat: float, lon: float, description: str, danger_level: str) -> bool:
        if any(wp['name'] == name for wp in self.waypoints):
            print(f"Error: Waypoint '{name}' already exists.")
            return False
        
        valid_danger_levels = {"Safe", "Caution", "Dangerous", "Death Trap"}
        if danger_level not in valid_danger_levels:
            print(f"Error: Invalid danger level '{danger_level}'. Must be one of {', '.join(valid_danger_levels)}.")
            return False

        waypoint = {
            'name': name,
            'lat': lat,
            'lon': lon,
            'description': description,
            'danger_level': danger_level
        }
        self.waypoints.append(waypoint)
        self._save_waypoints()
        print(f"Waypoint '{name}' added successfully.")
        return True

    def remove_waypoint(self, name: str) -> bool:
        initial_len = len(self.waypoints)
        self.waypoints = [wp for wp in self.waypoints if wp['name'] != name]
        if len(self.waypoints) < initial_len:
            self._save_waypoints()
            print(f"Waypoint '{name}' removed successfully.")
            return True
        else:
            print(f"Error: Waypoint '{name}' not found.")
            return False

    def list_waypoints(self):
        if not self.waypoints:
            print("No waypoints recorded yet. Add some with 'add' command.")
            return

        # Determine max width for each column
        name_width = max(len(wp['name']) for wp in self.waypoints) if self.waypoints else 4
        desc_width = max(len(wp['description']) for wp in self.waypoints) if self.waypoints else 11
        danger_width = max(len(wp['danger_level']) for wp in self.waypoints) if self.waypoints else 12

        # Ensure minimum widths for headers
        name_width = max(name_width, len("Name"))
        lat_width = max(len(str(round(wp['lat'], 4))) for wp in self.waypoints) if self.waypoints else 7 # e.g., 34.0522
        lon_width = max(len(str(round(wp['lon'], 4))) for wp in self.waypoints) if self.waypoints else 8 # e.g., -118.2437
        desc_width = max(desc_width, len("Description"))
        danger_width = max(danger_width, len("Danger Level"))

        header = f"{{:<{name_width}}} {{:> {lat_width}}} {{:> {lon_width}}} {{:<{desc_width}}} {{:<{danger_width}}}"
        print(header.format("Name", "Lat", "Lon", "Description", "Danger Level"))
        print("-" * (name_width + lat_width + lon_width + desc_width + danger_width + 4 * 3))

        for wp in self.waypoints:
            print(header.format(
                wp['name'],
                round(wp['lat'], 4),
                round(wp['lon'], 4),
                wp['description'],
                wp['danger_level']
            ))

def main():
    parser = argparse.ArgumentParser(
        description="Manage your wasteland waypoints.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new waypoint')
    add_parser.add_argument('--name', required=True, help='Unique name for the waypoint')
    add_parser.add_argument('--lat', type=float, required=True, help='Latitude coordinate')
    add_parser.add_argument('--lon', type=float, required=True, help='Longitude coordinate')
    add_parser.add_argument('--desc', required=True, help='A brief description of the location')
    add_parser.add_argument('--danger', required=True, 
                            choices=["Safe", "Caution", "Dangerous", "Death Trap"],
                            help='Danger level (Safe, Caution, Dangerous, Death Trap)')

    # List command
    list_parser = subparsers.add_parser('list', help='List all recorded waypoints')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a waypoint by name')
    remove_parser.add_argument('--name', required=True, help='Name of the waypoint to remove')

    args = parser.parse_args()

    manager = WaypointManager()

    if args.command == 'add':
        manager.add_waypoint(args.name, args.lat, args.lon, args.desc, args.danger)
    elif args.command == 'list':
        manager.list_waypoints()
    elif args.command == 'remove':
        manager.remove_waypoint(args.name)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
