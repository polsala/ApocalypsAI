import argparse
import json
import os
from datetime import date, timedelta

HOARD_FILE = 'hoard.json'
EXPIRY_WARNING_DAYS = 30

def load_hoard():
    """Loads the resource hoard from HOARD_FILE."""
    if not os.path.exists(HOARD_FILE):
        return {}
    try:
        with open(HOARD_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: '{HOARD_FILE}' is corrupted or empty. Starting with an empty hoard.")
        return {}

def save_hoard(hoard):
    """Saves the resource hoard to HOARD_FILE."""
    with open(HOARD_FILE, 'w') as f:
        json.dump(hoard, f, indent=4)

def add_item(hoard, name, quantity, expiry_date_str=None):
    """Adds or updates an item in the hoard."""
    if quantity <= 0:
        print(f"Error: Quantity to add for '{name}' must be positive.")
        return

    if name not in hoard:
        hoard[name] = {'quantity': 0, 'expiry': None}

    hoard[name]['quantity'] += quantity
    if expiry_date_str:
        # Validate date format
        try:
            date.fromisoformat(expiry_date_str)
            hoard[name]['expiry'] = expiry_date_str
        except ValueError:
            print(f"Warning: Invalid expiry date format for '{name}'. Expected YYYY-MM-DD. Not setting expiry.")
    print(f"Added {quantity} of '{name}'. Current quantity: {hoard[name]['quantity']}")

def remove_item(hoard, name, quantity):
    """Removes a specified quantity of an item from the hoard."""
    if quantity <= 0:
        print(f"Error: Quantity to remove for '{name}' must be positive.")
        return

    if name not in hoard:
        print(f"Error: '{name}' not found in hoard.")
        return

    if hoard[name]['quantity'] <= quantity:
        print(f"Removed all {hoard[name]['quantity']} of '{name}'. Item removed from hoard.")
        del hoard[name]
    else:
        hoard[name]['quantity'] -= quantity
        print(f"Removed {quantity} of '{name}'. Current quantity: {hoard[name]['quantity']}")

def list_items(hoard):
    """Lists all items in the hoard."""
    if not hoard:
        print("Your hoard is currently empty. Time to scavenge!")
        return

    print("\n--- Current Hoard Inventory ---")
    for name, data in hoard.items():
        expiry_info = f" (Expires: {data['expiry']})" if data['expiry'] else ""
        print(f"- {name}: {data['quantity']}{expiry_info}")
    print("-------------------------------\n")

def check_expiries(hoard, current_date=None):
    """Checks for items nearing their expiry date."""
    if current_date is None:
        current_date = date.today()

    expiring_soon = []
    for name, data in hoard.items():
        if data['expiry']:
            try:
                expiry_date = date.fromisoformat(data['expiry'])
                if current_date <= expiry_date < current_date + timedelta(days=EXPIRY_WARNING_DAYS):
                    expiring_soon.append((name, data['quantity'], data['expiry']))
            except ValueError:
                print(f"Warning: Malformed expiry date for '{name}': {data['expiry']}. Skipping expiry check.")

    if not expiring_soon:
        print("No items are expiring soon. Your hoard is secure for now!")
        return

    print(f"\n--- Items Expiring Within {EXPIRY_WARNING_DAYS} Days ---")
    for name, quantity, expiry in expiring_soon:
        print(f"- {name}: {quantity} (Expires: {expiry})")
    print("-------------------------------------------\n")

def main():
    parser = argparse.ArgumentParser(description="Manage your post-apocalyptic resource hoard.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add items to the hoard.')
    add_parser.add_argument('name', type=str, help='Name of the item.')
    add_parser.add_argument('quantity', type=int, help='Quantity to add.')
    add_parser.add_argument('expiry', type=str, nargs='?', help='Optional expiry date (YYYY-MM-DD).')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove items from the hoard.')
    remove_parser.add_argument('name', type=str, help='Name of the item.')
    remove_parser.add_argument('quantity', type=int, help='Quantity to remove.')

    # List command
    subparsers.add_parser('list', help='List all items in the hoard.')

    # Check expiry command
    subparsers.add_parser('check-expiry', help='Check for items nearing expiry.')

    args = parser.parse_args()

    hoard = load_hoard()

    if args.command == 'add':
        add_item(hoard, args.name, args.quantity, args.expiry)
    elif args.command == 'remove':
        remove_item(hoard, args.name, args.quantity)
    elif args.command == 'list':
        list_items(hoard)
    elif args.command == 'check-expiry':
        check_expiries(hoard)
    else:
        parser.print_help()
        return # Exit if no valid command or help is printed

    if args.command in ['add', 'remove']:
        save_hoard(hoard)

if __name__ == '__main__':
    main()
