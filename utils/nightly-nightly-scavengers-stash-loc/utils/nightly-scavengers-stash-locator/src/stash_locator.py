import json
import os
import argparse

class StashLocator:
    def __init__(self, data_file="stashes.json"):
        self.data_file = data_file
        self.stashes = self._load_stashes()

    def _load_stashes(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {self.data_file} is corrupted. Starting with an empty stash list.")
                return []
        return []

    def _save_stashes(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.stashes, f, indent=4)

    def add_stash(self, name, description, coords):
        if any(s['name'].lower() == name.lower() for s in self.stashes):
            return False, f"Stash '{name}' already exists."
        self.stashes.append({
            "name": name,
            "description": description,
            "coordinates": coords
        })
        self._save_stashes()
        return True, f"Stash '{name}' added."

    def list_stashes(self):
        return self.stashes

    def find_stash(self, name):
        for stash in self.stashes:
            if stash['name'].lower() == name.lower():
                return stash
        return None

    def remove_stash(self, name):
        initial_len = len(self.stashes)
        self.stashes = [s for s in self.stashes if s['name'].lower() != name.lower()]
        if len(self.stashes) < initial_len:
            self._save_stashes()
            return True, f"Stash '{name}' removed."
        return False, f"Stash '{name}' not found."

def main():
    parser = argparse.ArgumentParser(description="Manage your scavenger stashes.")
    parser.add_argument("--data-file", default="stashes.json", help="Path to the JSON data file.")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new stash.")
    add_parser.add_argument("name", help="Name of the stash.")
    add_parser.add_argument("description", help="Description of the stash.")
    add_parser.add_argument("coordinates", help="Coordinates of the stash (e.g., 'X:123,Y:456').")

    # List command
    list_parser = subparsers.add_parser("list", help="List all stashes.")

    # Find command
    find_parser = subparsers.add_parser("find", help="Find a stash by name.")
    find_parser.add_argument("name", help="Name of the stash to find.")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a stash by name.")
    remove_parser.add_argument("name", help="Name of the stash to remove.")

    args = parser.parse_args()

    locator = StashLocator(args.data_file)

    if args.command == "add":
        success, message = locator.add_stash(args.name, args.description, args.coordinates)
        print(message)
    elif args.command == "list":
        stashes = locator.list_stashes()
        if stashes:
            print("--- Your Stashes ---")
            for stash in stashes:
                print(f"Name: {stash['name']}")
                print(f"  Description: {stash['description']}")
                print(f"  Coordinates: {stash['coordinates']}")
                print("-" * 20)
        else:
            print("No stashes found. Add some with 'add' command!")
    elif args.command == "find":
        stash = locator.find_stash(args.name)
        if stash:
            print(f"--- Stash Found: {stash['name']} ---")
            print(f"  Description: {stash['description']}")
            print(f"  Coordinates: {stash['coordinates']}")
        else:
            print(f"Stash '{args.name}' not found.")
    elif args.command == "remove":
        success, message = locator.remove_stash(args.name)
        print(message)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
