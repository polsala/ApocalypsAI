import argparse
import json
import os

DATA_FILE = "supplies.json"

def _get_data_path():
    """Returns the absolute path to the data file."""
    # This ensures the data file is always in the same directory as the script
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_FILE)

def load_data():
    """Loads supply data from the JSON file."""
    data_path = _get_data_path()
    if not os.path.exists(data_path):
        return {"locations": {}}
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {DATA_FILE} is corrupted. Starting with empty data.")
        return {"locations": {}}

def save_data(data):
    """Saves supply data to the JSON file."""
    data_path = _get_data_path()
    with open(data_path, 'w') as f:
        json.dump(data, f, indent=4)

def add_supply(location: str, item: str, quantity: int):
    """Adds or updates a supply item in a specific location."""
    data = load_data()
    location = location.capitalize()
    item = item.capitalize()

    if location not in data["locations"]:
        data["locations"][location] = []

    found = False
    for supply in data["locations"][location]:
        if supply["item"] == item:
            supply["quantity"] += quantity
            found = True
            break
    if not found:
        data["locations"][location].append({"item": item, "quantity": quantity})

    save_data(data)
    print(f"Added {quantity}x {item} to {location}.")

def list_supplies(location: str = None):
    """Lists all supplies or supplies for a specific location."""
    data = load_data()
    locations_to_list = []

    if location:
        location = location.capitalize()
        if location in data["locations"]:
            locations_to_list.append(location)
        else:
            print(f"Location '{location}' not found.")
            return
    else:
        locations_to_list = sorted(data["locations"].keys())

    if not locations_to_list:
        print("No supplies tracked yet. Go scavenge!")
        return

    for loc in locations_to_list:
        print(f"\n--- {loc} ---")
        if not data["locations"][loc]:
            print("  (Empty)")
            continue
        for supply in sorted(data["locations"][loc], key=lambda x: x['item']):
            print(f"  - {supply['item']}: {supply['quantity']}")

def remove_supply(location: str, item: str, quantity: int = None):
    """Removes a specific supply item from a location, or reduces its quantity."""
    data = load_data()
    location = location.capitalize()
    item = item.capitalize()

    if location not in data["locations"]:
        print(f"Location '{location}' not found.")
        return

    found_index = -1
    for i, supply in enumerate(data["locations"][location]):
        if supply["item"] == item:
            found_index = i
            break

    if found_index == -1:
        print(f"Item '{item}' not found in '{location}'.")
        return

    if quantity is None or quantity >= data["locations"][location][found_index]["quantity"]:
        removed_qty = data["locations"][location][found_index]["quantity"]
        data["locations"][location].pop(found_index)
        print(f"Removed all {removed_qty}x {item} from {location}.")
    else:
        data["locations"][location][found_index]["quantity"] -= quantity
        print(f"Removed {quantity}x {item} from {location}. Remaining: {data['locations'][location][found_index]['quantity']}x.")

    # Clean up empty locations
    if not data["locations"][location]:
        del data["locations"][location]

    save_data(data)


def main():
    parser = argparse.ArgumentParser(
        description="Scavenger's Supply Tracker: Keep tabs on your post-apocalyptic loot!",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add or update a supply item.")
    add_parser.add_argument("location", type=str, help="The location where the supply was found (e.g., 'Old Supermarket').")
    add_parser.add_argument("item", type=str, help="The name of the supply item (e.g., 'Canned Beans').")
    add_parser.add_argument("quantity", type=int, help="The quantity of the item to add.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all supplies or supplies for a specific location.")
    list_parser.add_argument("--location", type=str, help="Optional: Filter supplies by a specific location.")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a supply item or reduce its quantity.")
    remove_parser.add_argument("location", type=str, help="The location from which to remove the supply.")
    remove_parser.add_argument("item", type=str, help="The name of the supply item to remove.")
    remove_parser.add_argument("--quantity", type=int,
                                help="Optional: The quantity to remove. If not specified, all of the item will be removed.")

    args = parser.parse_args()

    if args.command == "add":
        if args.quantity <= 0:
            print("Quantity must be a positive integer.")
            return
        add_supply(args.location, args.item, args.quantity)
    elif args.command == "list":
        list_supplies(args.location)
    elif args.command == "remove":
        if args.quantity is not None and args.quantity <= 0:
            print("Quantity to remove must be a positive integer.")
            return
        remove_supply(args.location, args.item, args.quantity)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
