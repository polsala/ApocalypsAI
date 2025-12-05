import argparse
import json
import os
import sys

STASH_FILENAME = "scavenger_stash.json"

def get_default_stash_path():
    """Determines the default path for the stash file."""
    # For simplicity, store in the current working directory.
    # In a real-world scenario, consider user's config directory (e.g., ~/.config/apocalypsai)
    return os.path.join(os.getcwd(), STASH_FILENAME)

def load_stash(file_path):
    """Loads the stash from a JSON file."""
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Stash file '{file_path}' is corrupted. Starting with an empty stash.", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Error loading stash from '{file_path}': {e}", file=sys.stderr)
        return {}

def save_stash(file_path, stash):
    """Saves the stash to a JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(stash, f, indent=4)
    except Exception as e:
        print(f"Error saving stash to '{file_path}': {e}", file=sys.stderr)

def add_item(item_name, quantity, file_path):
    """Adds or updates an item in the stash."""
    stash = load_stash(file_path)
    item_name_lower = item_name.lower()
    if item_name_lower in stash:
        stash[item_name_lower]['quantity'] += quantity
        print(f"Updated '{item_name}': new quantity is {stash[item_name_lower]['quantity']}")
    else:
        stash[item_name_lower] = {'name': item_name, 'quantity': quantity}
        print(f"Added '{item_name}' with quantity {quantity}")
    save_stash(file_path, stash)

def list_items(file_path):
    """Lists all items in the stash."""
    stash = load_stash(file_path)
    if not stash:
        print("Your scavenger's stash is empty. Time to forage!")
        return

    print("\n--- Your Scavenger's Stash ---")
    for item_data in stash.values():
        print(f"- {item_data['name']}: {item_data['quantity']}")
    print("----------------------------\n")

def remove_item(item_name, file_path):
    """Removes an item from the stash."""
    stash = load_stash(file_path)
    item_name_lower = item_name.lower()
    if item_name_lower in stash:
        del stash[item_name_lower]
        save_stash(file_path, stash)
        print(f"Removed '{item_name}' from your stash.")
    else:
        print(f"'{item_name}' not found in your stash.")

def clear_stash(file_path):
    """Clears all items from the stash."""
    save_stash(file_path, {})
    print("Your scavenger's stash has been cleared. A fresh start!")

def main():
    parser = argparse.ArgumentParser(
        description="Track your scavenged resources in the post-apocalyptic wasteland.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--stash-file',
        default=get_default_stash_path(),
        help=f"Path to the stash JSON file (default: {STASH_FILENAME} in current directory)."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add or update an item in the stash.')
    add_parser.add_argument('item', type=str, help='Name of the item.')
    add_parser.add_argument('quantity', type=int, help='Quantity of the item (can be negative to reduce).')

    # List command
    list_parser = subparsers.add_parser('list', help='List all items in the stash.')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove an item from the stash.')
    remove_parser.add_argument('item', type=str, help='Name of the item to remove.')

    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear all items from the stash.')

    args = parser.parse_args()

    if args.command == 'add':
        add_item(args.item, args.quantity, args.stash_file)
    elif args.command == 'list':
        list_items(args.stash_file)
    elif args.command == 'remove':
        remove_item(args.item, args.stash_file)
    elif args.command == 'clear':
        clear_stash(args.stash_file)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
