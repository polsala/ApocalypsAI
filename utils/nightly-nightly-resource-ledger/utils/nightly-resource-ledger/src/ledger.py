import argparse
import json
import os
from collections import defaultdict

LEDGER_FILE = "resources.json"

def load_ledger(file_path=LEDGER_FILE):
    """Loads the resource ledger from a JSON file."""
    if not os.path.exists(file_path):
        return defaultdict(int)
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Ensure all values are integers, convert if necessary
            return defaultdict(int, {k: int(v) for k, v in data.items()})
    except json.JSONDecodeError:
        print(f"Warning: {file_path} is corrupted or empty. Starting with an empty ledger.")
        return defaultdict(int)
    except Exception as e:
        print(f"Error loading ledger from {file_path}: {e}. Starting with an empty ledger.")
        return defaultdict(int)

def save_ledger(ledger, file_path=LEDGER_FILE):
    """Saves the resource ledger to a JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(dict(ledger), f, indent=4)
    except Exception as e:
        print(f"Error saving ledger to {file_path}: {e}")

def add_resource(resource_name, quantity, location=None, file_path=LEDGER_FILE):
    """Adds a resource to the ledger."""
    ledger = load_ledger(file_path)
    if quantity <= 0:
        print(f"Scavenger's wisdom: Quantity must be positive to add a resource, not {quantity}.")
        return

    ledger[resource_name] += quantity
    save_ledger(ledger, file_path)
    loc_info = f" (found at {location})" if location else ""
    print(f"Added {quantity} unit(s) of '{resource_name}' to your stash{loc_info}. Total: {ledger[resource_name]}.")

def remove_resource(resource_name, quantity, file_path=LEDGER_FILE):
    """Removes a resource from the ledger."""
    ledger = load_ledger(file_path)
    if quantity <= 0:
        print(f"Scavenger's wisdom: Quantity must be positive to remove a resource, not {quantity}.")
        return
    if resource_name not in ledger or ledger[resource_name] == 0:
        print(f"No '{resource_name}' found in your ledger to remove. Perhaps it was already consumed?")
        return

    if ledger[resource_name] < quantity:
        print(f"Warning: You only have {ledger[resource_name]} unit(s) of '{resource_name}'. Removing all of them.")
        ledger[resource_name] = 0
    else:
        ledger[resource_name] -= quantity
    
    if ledger[resource_name] == 0:
        del ledger[resource_name] # Clean up empty entries
        print(f"All '{resource_name}' consumed. It's gone.")
    else:
        print(f"Removed {quantity} unit(s) of '{resource_name}'. Remaining: {ledger[resource_name]}.")
    save_ledger(ledger, file_path)

def list_resources(file_path=LEDGER_FILE):
    """Lists all resources in the ledger."""
    ledger = load_ledger(file_path)
    if not ledger:
        print("Your ledger is empty. Time to scavenge!")
        return

    print("\n--- Your Wasteland Stash ---")
    for name, quantity in sorted(ledger.items()):
        print(f"- {name}: {quantity} unit(s)")
    print("---------------------------\n")

def show_resource(resource_name, file_path=LEDGER_FILE):
    """Shows the total quantity of a specific resource."""
    ledger = load_ledger(file_path)
    quantity = ledger.get(resource_name, 0)
    if quantity > 0:
        print(f"You have {quantity} unit(s) of '{resource_name}'.")
    else:
        print(f"No '{resource_name}' found in your ledger. Keep an eye out!")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Resource Ledger: Track your scavenged goods.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a resource to the ledger.")
    add_parser.add_argument("name", type=str, help="Name of the resource (e.g., 'Canned Beans').")
    add_parser.add_argument("quantity", type=int, help="Quantity to add.")
    add_parser.add_argument("--location", type=str, help="Optional: Where the resource was found.")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a resource from the ledger.")
    remove_parser.add_argument("name", type=str, help="Name of the resource to remove.")
    remove_parser.add_argument("quantity", type=int, help="Quantity to remove.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all resources in the ledger.")

    # Show command
    show_parser = subparsers.add_parser("show", help="Show the total quantity of a specific resource.")
    show_parser.add_argument("name", type=str, help="Name of the resource to show.")

    args = parser.parse_args()

    if args.command == "add":
        add_resource(args.name, args.quantity, args.location)
    elif args.command == "remove":
        remove_resource(args.name, args.quantity)
    elif args.command == "list":
        list_resources()
    elif args.command == "show":
        show_resource(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
