import argparse
import json
import os
import sys

LEDGER_FILE = "scavenger_ledger.json"

def load_ledger(file_path=LEDGER_FILE):
    """Loads the ledger data from a JSON file."""
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Ledger file '{file_path}' is corrupted. Starting with an empty ledger.", file=sys.stderr)
        return {} # Handle corrupted JSON
    except Exception as e:
        print(f"Error loading ledger from '{file_path}': {e}", file=sys.stderr)
        return {}

def save_ledger(ledger, file_path=LEDGER_FILE):
    """Saves the ledger data to a JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(ledger, f, indent=4)
    except Exception as e:
        print(f"Error saving ledger to '{file_path}': {e}", file=sys.stderr)

def add_item(item_name, qty, condition, notes, file_path=LEDGER_FILE):
    """Adds a new item to the ledger."""
    ledger = load_ledger(file_path)
    if item_name in ledger:
        print(f"Warning: Item '{item_name}' already exists. Use 'update' to modify it.")
        return False
    ledger[item_name] = {"qty": qty, "condition": condition, "notes": notes}
    save_ledger(ledger, file_path)
    print(f"Added '{item_name}' to the ledger.")
    return True

def update_item(item_name, qty, condition, notes, file_path=LEDGER_FILE):
    """Updates an existing item in the ledger."""
    ledger = load_ledger(file_path)
    if item_name not in ledger:
        print(f"Error: Item '{item_name}' not found. Use 'add' to create it.")
        return False
    
    item_data = ledger[item_name]
    if qty is not None:
        item_data["qty"] = qty
    if condition is not None:
        item_data["condition"] = condition
    if notes is not None:
        item_data["notes"] = notes
        
    save_ledger(ledger, file_path)
    print(f"Updated '{item_name}' in the ledger.")
    return True

def remove_item(item_name, file_path=LEDGER_FILE):
    """Removes an item from the ledger."""
    ledger = load_ledger(file_path)
    if item_name not in ledger:
        print(f"Error: Item '{item_name}' not found.")
        return False
    del ledger[item_name]
    save_ledger(ledger, file_path)
    print(f"Removed '{item_name}' from the ledger.")
    return True

def list_items(file_path=LEDGER_FILE):
    """Lists all items in the ledger."""
    ledger = load_ledger(file_path)
    if not ledger:
        print("The scavenger's ledger is empty. Time to scavenge!")
        return
    print("\n--- Scavenger's Supply Ledger ---")
    for item, details in ledger.items():
        print(f"  Item: {item}")
        print(f"    Qty: {details['qty']}")
        print(f"    Condition: {details['condition']}")
        print(f"    Notes: {details['notes']}")
        print("-" * 30)
    print("---------------------------------\n")

def main():
    parser = argparse.ArgumentParser(
        description="Manage your post-apocalyptic scavenger's supply ledger."
    )
    parser.add_argument(
        "--ledger-file",
        default=LEDGER_FILE,
        help=f"Path to the ledger JSON file (default: {LEDGER_FILE})"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new item to the ledger.")
    add_parser.add_argument("item_name", help="Name of the item.")
    add_parser.add_argument("--qty", type=int, default=1, help="Quantity of the item.")
    add_parser.add_argument("--condition", default="unknown", help="Condition of the item (e.g., 'new', 'used', 'broken').")
    add_parser.add_argument("--notes", default="", help="Any additional notes about the item.")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing item in the ledger.")
    update_parser.add_argument("item_name", help="Name of the item to update.")
    update_parser.add_argument("--qty", type=int, help="New quantity of the item.")
    update_parser.add_argument("--condition", help="New condition of the item.")
    update_parser.add_argument("--notes", help="New notes about the item.")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove an item from the ledger.")
    remove_parser.add_argument("item_name", help="Name of the item to remove.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all items in the ledger.")

    args = parser.parse_args()

    if args.command == "add":
        add_item(args.item_name, args.qty, args.condition, args.notes, args.ledger_file)
    elif args.command == "update":
        update_item(args.item_name, args.qty, args.condition, args.notes, args.ledger_file)
    elif args.command == "remove":
        remove_item(args.item_name, args.ledger_file)
    elif args.command == "list":
        list_items(args.ledger_file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
