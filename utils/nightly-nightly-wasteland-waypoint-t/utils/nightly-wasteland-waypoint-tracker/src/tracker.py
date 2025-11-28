import json
import os
import argparse
import time
from datetime import datetime

class WaypointTracker:
    def __init__(self, data_file='waypoints.json'):
        self.data_file = data_file
        self.waypoints = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {self.data_file} is corrupted or empty. Starting with an empty waypoint list.")
            return []
        except Exception as e:
            print(f"Error loading data from {self.data_file}: {e}")
            return []

    def _save_data(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.waypoints, f, indent=4)
        except Exception as e:
            print(f"Error saving data to {self.data_file}: {e}")

    def add_waypoint(self, name, target, tags=None, description=None):
        waypoint_id = int(time.time() * 1000) # Unique ID based on timestamp
        timestamp = datetime.now().isoformat()
        new_waypoint = {
            'id': waypoint_id,
            'name': name,
            'target': target,
            'tags': [tag.strip() for tag in tags.split(',')] if tags else [],
            'description': description if description else '',
            'created_at': timestamp
        }
        self.waypoints.append(new_waypoint)
        self._save_data()
        print(f"Waypoint '{name}' (ID: {waypoint_id}) added successfully.")
        return new_waypoint

    def list_waypoints(self):
        if not self.waypoints:
            print("No waypoints found. Start by adding one!")
            return []
        print("\n--- Your Wasteland Waypoints ---")
        for wp in self.waypoints:
            print(f"ID: {wp['id']}")
            print(f"  Name: {wp['name']}")
            print(f"  Target: {wp['target']}")
            print(f"  Tags: {', '.join(wp['tags']) if wp['tags'] else 'None'}")
            print(f"  Description: {wp['description']}")
            print(f"  Created: {wp['created_at']}")
            print("-------------------------------")
        return self.waypoints

    def search_waypoints(self, query):
        query_lower = query.lower()
        results = []
        for wp in self.waypoints:
            if (query_lower in wp['name'].lower() or
                query_lower in wp['target'].lower() or
                query_lower in wp['description'].lower() or
                any(query_lower in tag.lower() for tag in wp['tags'])):
                results.append(wp)
        
        if not results:
            print(f"No waypoints found matching '{query}'.")
            return []

        print(f"\n--- Search Results for '{query}' ---")
        for wp in results:
            print(f"ID: {wp['id']}")
            print(f"  Name: {wp['name']}")
            print(f"  Target: {wp['target']}")
            print(f"  Tags: {', '.join(wp['tags']) if wp['tags'] else 'None'}")
            print(f"  Description: {wp['description']}")
            print(f"  Created: {wp['created_at']}")
            print("-------------------------------")
        return results

    def delete_waypoint(self, waypoint_id):
        initial_count = len(self.waypoints)
        self.waypoints = [wp for wp in self.waypoints if wp['id'] != waypoint_id]
        if len(self.waypoints) < initial_count:
            self._save_data()
            print(f"Waypoint with ID '{waypoint_id}' deleted successfully.")
            return True
        else:
            print(f"No waypoint found with ID '{waypoint_id}'.")
            return False

def main():
    parser = argparse.ArgumentParser(description="Wasteland Waypoint Tracker: Keep track of important paths, URLs, and notes.")
    parser.add_argument('--data-file', default='waypoints.json', help="Specify the JSON file to store waypoints.")

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new waypoint')
    add_parser.add_argument('--name', required=True, help='A short, descriptive name for the waypoint.')
    add_parser.add_argument('--target', required=True, help='The path or URL of the waypoint.')
    add_parser.add_argument('--tags', help='Comma-separated tags (e.g., config,api,docs).')
    add_parser.add_argument('--description', help='A longer description of the waypoint.')

    # List command
    list_parser = subparsers.add_parser('list', help='List all waypoints')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search waypoints by name, target, description, or tags.')
    search_parser.add_argument('query', help='The search query.')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a waypoint by its ID.')
    delete_parser.add_argument('--id', type=int, required=True, help='The ID of the waypoint to delete.')

    args = parser.parse_args()

    tracker = WaypointTracker(args.data_file)

    if args.command == 'add':
        tracker.add_waypoint(args.name, args.target, args.tags, args.description)
    elif args.command == 'list':
        tracker.list_waypoints()
    elif args.command == 'search':
        tracker.search_waypoints(args.query)
    elif args.command == 'delete':
        tracker.delete_waypoint(args.id)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
