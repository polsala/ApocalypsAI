import json
import os
import sys
import argparse

# Define the manifest file name
MANIFEST_FILE = 'manifest.json'

def _get_manifest_path():
    """Returns the absolute path to the manifest file."""
    # This ensures the manifest.json is created/read in the same directory as the script
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), MANIFEST_FILE)

def _load_manifest():
    """Loads the manifest data from the JSON file."""
    manifest_path = _get_manifest_path()
    if not os.path.exists(manifest_path):
        return {"items": []}
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {MANIFEST_FILE} is corrupted. Starting with an empty manifest.", file=sys.stderr)
        return {"items": []}
    except Exception as e:
        print(f"Error loading manifest: {e}", file=sys.stderr)
        return {"items": []}

def _save_manifest(data):
    """Saves the manifest data to the JSON file."""
    manifest_path = _get_manifest_path()
    try:
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving manifest: {e}", file=sys.stderr)

def add_item(name: str, category: str, quantity: int):
    """Adds a new item or updates an existing one in the manifest."""
    manifest = _load_manifest()
    
    # Normalize name for case-insensitive comparison
    normalized_name = name.lower()

    found = False
    for item in manifest["items"]:
        if item["name"].lower() == normalized_name:
            item["category"] = category # Update category if item exists
            item["quantity"] += quantity # Add to existing quantity
            found = True
            break
    
    if not found:
        manifest["items"].append({"name": name, "category": category, "quantity": quantity})
    
    _save_manifest(manifest)
    print(f"Added/Updated: {name} ({category}, Qty: {quantity})")

def list_items():
    """Lists all items currently in the manifest."""
    manifest = _load_manifest()
    if not manifest["items"]:
        print("Your manifest is currently empty. Go scavenge!")
        return

    print("--- Current Manifest ---")
    for item in manifest["items"]:
        print(f"Name: {item['name']}, Category: {item['category']}, Quantity: {item['quantity']}")
    print("------------------------")

def search_items(keyword: str):
    """Searches for items by name or category using a keyword."""
    manifest = _load_manifest()
    normalized_keyword = keyword.lower()
    
    results = [
        item for item in manifest["items"]
        if normalized_keyword in item["name"].lower() or normalized_keyword in item["category"].lower()
    ]

    if not results:
        print(f"No items found matching '{keyword}'.")
        return

    print(f"--- Search Results for '{keyword}' ---")
    for item in results:
        print(f"Name: {item['name']}, Category: {item['category']}, Quantity: {item['quantity']}")
    print("------------------------------------")

def main():
    parser = argparse.ArgumentParser(
        description="Manage your scavenger's manifest of found items."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new item or update an existing one.")
    add_parser.add_argument("name", type=str, help="Name of the item.")
    add_parser.add_argument("category", type=str, help="Category of the item (e.g., Food, Tools, Weapons).")
    add_parser.add_argument("quantity", type=int, help="Quantity of the item.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all items in the manifest.")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for items by name or category.")
    search_parser.add_argument("keyword", type=str, help="Keyword to search for.")

    args = parser.parse_args()

    if args.command == "add":
        if args.quantity <= 0:
            print("Quantity must be a positive integer.", file=sys.stderr)
            sys.exit(1)
        add_item(args.name, args.category, args.quantity)
    elif args.command == "list":
        list_items()
    elif args.command == "search":
        search_items(args.keyword)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
