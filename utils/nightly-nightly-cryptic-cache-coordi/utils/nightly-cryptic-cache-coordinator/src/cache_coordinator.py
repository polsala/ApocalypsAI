import argparse
import json
import os
from typing import Dict, List, Any

CACHE_FILE = 'caches.json'

def _load_caches() -> Dict[str, Any]:
    """Loads caches from the JSON file."""
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {CACHE_FILE} is corrupted. Starting with an empty cache.")
        return {}

def _save_caches(caches: Dict[str, Any]):
    """Saves caches to the JSON file."""
    with open(CACHE_FILE, 'w') as f:
        json.dump(caches, f, indent=4)

def add_cache(name: str, location: str, hint: str):
    """Adds a new cache entry."""
    caches = _load_caches()
    if name in caches:
        print(f"Error: Cache '{name}' already exists. Use 'update' if you want to modify it (not implemented yet).")
        return

    caches[name] = {
        'location': location,
        'hint': hint
    }
    _save_caches(caches)
    print(f"Cache '{name}' added successfully.")

def list_caches():
    """Lists all stored cache names."""
    caches = _load_caches()
    if not caches:
        print("No caches found. Time to start hiding some treasures!")
        return

    print("\n--- Your Cryptic Caches ---")
    for name in caches:
        print(f"- {name}")
    print("---------------------------\n")

def view_cache(name: str):
    """Displays details for a specific cache."""
    caches = _load_caches()
    cache = caches.get(name)
    if not cache:
        print(f"Error: Cache '{name}' not found.")
        return

    print(f"\n--- Cache Details for '{name}' ---")
    print(f"Location: {cache['location']}")
    print(f"Hint: {cache['hint']}")
    print("-----------------------------------\n")

def delete_cache(name: str):
    """Deletes a cache entry."""
    caches = _load_caches()
    if name not in caches:
        print(f"Error: Cache '{name}' not found.")
        return

    del caches[name]
    _save_caches(caches)
    print(f"Cache '{name}' deleted successfully.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cryptic Cache Coordinator: Manage your hidden treasures."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new cache entry.')
    add_parser.add_argument('--name', required=True, help='Name of the cache.')
    add_parser.add_argument('--location', required=True, help='Physical location of the cache.')
    add_parser.add_argument('--hint', required=True, help='A cryptic hint to remember the cache.')

    # List command
    list_parser = subparsers.add_parser('list', help='List all stored cache names.')

    # View command
    view_parser = subparsers.add_parser('view', help='View details for a specific cache.')
    view_parser.add_argument('--name', required=True, help='Name of the cache to view.')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a cache entry.')
    delete_parser.add_argument('--name', required=True, help='Name of the cache to delete.')

    args = parser.parse_args()

    if args.command == 'add':
        add_cache(args.name, args.location, args.hint)
    elif args.command == 'list':
        list_caches()
    elif args.command == 'view':
        view_cache(args.name)
    elif args.command == 'delete':
        delete_cache(args.name)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
