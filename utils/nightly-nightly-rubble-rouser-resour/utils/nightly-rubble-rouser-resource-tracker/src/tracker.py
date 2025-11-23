import json
import os
import argparse
from collections import defaultdict

DATA_FILE = "resources.json"

def load_resources(data_file=DATA_FILE):
    """Loads resources from the JSON data file."""
    if not os.path.exists(data_file):
        return {}
    with open(data_file, 'r') as f:
        return json.load(f)

def save_resources(resources, data_file=DATA_FILE):
    """Saves resources to the JSON data file."""
    with open(data_file, 'w') as f:
        json.dump(resources, f, indent=4)

def add_resource(stash_name, item_name, quantity, data_file=DATA_FILE):
    """Adds or updates a resource in a specific stash."""
    resources = load_resources(data_file)
    if stash_name not in resources:
        resources[stash_name] = {}
    resources[stash_name][item_name] = resources[stash_name].get(item_name, 0) + quantity
    save_resources(resources, data_file)
    return f"Added {quantity} of {item_name} to {stash_name}. New total: {resources[stash_name][item_name]}"

def remove_resource(stash_name, item_name, quantity, data_file=DATA_FILE):
    """Removes a specified quantity of a resource from a stash."""
    resources = load_resources(data_file)
    if stash_name not in resources or item_name not in resources[stash_name]:
        return f"Error: {item_name} not found in {stash_name}."
    
    current_quantity = resources[stash_name][item_name]
    if quantity >= current_quantity:
        del resources[stash_name][item_name]
        if not resources[stash_name]: # Remove stash if empty
            del resources[stash_name]
        save_resources(resources, data_file)
        return f"Removed all {current_quantity} of {item_name} from {stash_name}."
    else:
        resources[stash_name][item_name] -= quantity
        save_resources(resources, data_file)
        return f"Removed {quantity} of {item_name} from {stash_name}. Remaining: {resources[stash_name][item_name]}"

def get_summary(data_file=DATA_FILE):
    """Provides a summary of all resources across all stashes."""
    resources = load_resources(data_file)
    if not resources:
        return "No resources tracked yet. Start adding some!"

    summary_lines = ["--- Resource Summary ---"]
    total_items = defaultdict(int)

    for stash, items in resources.items():
        summary_lines.append(f"\nStash: {stash}")
        if not items:
            summary_lines.append("  (Empty)")
            continue
        for item, quantity in items.items():
            summary_lines.append(f"  - {item}: {quantity}")
            total_items[item] += quantity
    
    summary_lines.append("\n--- Global Totals ---")
    if not total_items:
        summary_lines.append("No items globally.")
    else:
        for item, quantity in sorted(total_items.items()):
            summary_lines.append(f"  - {item}: {quantity}")
    
    return "\n".join(summary_lines)

def get_low_stock_alerts(threshold, data_file=DATA_FILE):
    """Identifies resources with quantities below a specified threshold."""
    resources = load_resources(data_file)
    if not resources:
        return "No resources tracked yet. No low stock alerts."

    alerts = []
    for stash, items in resources.items():
        for item, quantity in items.items():
            if quantity < threshold:
                alerts.append(f"LOW STOCK: {item} in {stash} has only {quantity} left (threshold: {threshold})")
    
    if not alerts:
        return f"All resources are above the low stock threshold of {threshold}."
    
    return "\n".join(["--- Low Stock Alerts ---"] + alerts)

def main():
    parser = argparse.ArgumentParser(
        description="Rubble-Rouser Resource Tracker: Manage your scavenged supplies across different stashes."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add or update a resource.")
    add_parser.add_argument("stash", help="Name of the stash (e.g., 'Garage', 'Basement').")
    add_parser.add_argument("item", help="Name of the resource item (e.g., 'Water Bottle', 'Canned Beans').")
    add_parser.add_argument("quantity", type=int, help="Quantity to add.")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a resource quantity.")
    remove_parser.add_argument("stash", help="Name of the stash.")
    remove_parser.add_argument("item", help="Name of the resource item.")
    remove_parser.add_argument("quantity", type=int, help="Quantity to remove.")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Get a summary of all resources.")

    # Alerts command
    alerts_parser = subparsers.add_parser("alerts", help="Get low stock alerts.")
    alerts_parser.add_argument("--threshold", type=int, default=5,
                               help="Quantity threshold for low stock alerts (default: 5).")

    args = parser.parse_args()

    if args.command == "add":
        print(add_resource(args.stash, args.item, args.quantity))
    elif args.command == "remove":
        print(remove_resource(args.stash, args.item, args.quantity))
    elif args.command == "summary":
        print(get_summary())
    elif args.command == "alerts":
        print(get_low_stock_alerts(args.threshold))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
