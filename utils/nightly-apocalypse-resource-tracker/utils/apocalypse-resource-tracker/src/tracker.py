import argparse
import json
import os
from datetime import datetime

DATA_FILE = 'resources.json'

def get_data_file_path():
    """Returns the absolute path to the data file."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_FILE)

def load_resources():
    """Loads resources from the JSON data file."""
    file_path = get_data_file_path()
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {DATA_FILE} is corrupted. Starting with an empty inventory.")
        return []

def save_resources(resources):
    """Saves resources to the JSON data file."""
    file_path = get_data_file_path()
    with open(file_path, 'w') as f:
        json.dump(resources, f, indent=2)

def add_item(name, quantity, expires=None, location=None):
    """Adds a new item or updates an existing one."""
    resources = load_resources()
    quantity = int(quantity)
    if quantity <= 0:
        print("Quantity must be positive.")
        return

    found = False
    for item in resources:
        if item['name'].lower() == name.lower():
            item['quantity'] += quantity
            if expires: item['expires'] = expires # Update if provided
            if location: item['location'] = location # Update if provided
            found = True
            break
    
    if not found:
        resources.append({
            'name': name,
            'quantity': quantity,
            'expires': expires,
            'location': location
        })
    
    save_resources(resources)
    print(f"Added {quantity}x {name}. Current stock: {next((item['quantity'] for item in resources if item['name'].lower() == name.lower()), quantity)}.")

def consume_item(name, quantity):
    """Consumes a quantity of an existing item."""
    resources = load_resources()
    quantity = int(quantity)
    if quantity <= 0:
        print("Quantity must be positive.")
        return

    found = False
    for item in resources:
        if item['name'].lower() == name.lower():
            if item['quantity'] < quantity:
                print(f"Not enough {name} to consume. Only {item['quantity']} available.")
                return
            item['quantity'] -= quantity
            found = True
            break
    
    if not found:
        print(f"Item '{name}' not found in inventory.")
        return

    # Remove item if quantity drops to 0 or less
    resources = [item for item in resources if item['quantity'] > 0]
    
    save_resources(resources)
    print(f"Consumed {quantity}x {name}. Current stock: {next((item['quantity'] for item in resources if item['name'].lower() == name.lower()), 0)}.")

def list_items():
    """Lists all items in the inventory."""
    resources = load_resources()
    if not resources:
        print("Your inventory is empty. Time to scavenge!")
        return

    print("\n--- Current Inventory ---")
    print(f"{'Item':<30} {'Qty':<5} {'Expires':<12} {'Location':<20}")
    print("-" * 70)

    today = datetime.now().date()

    for item in sorted(resources, key=lambda x: x['name'].lower()):
        name = item['name']
        qty = item['quantity']
        expires = item['expires'] if item['expires'] else 'N/A'
        location = item['location'] if item['location'] else 'N/A'

        status_indicator = ""
        if expires != 'N/A':
            try:
                exp_date = datetime.strptime(expires, '%Y-%m-%d').date()
                if exp_date < today:
                    status_indicator = " (EXPIRED!)"
                elif (exp_date - today).days <= 30:
                    status_indicator = " (Expiring soon!)"
            except ValueError:
                pass # Malformed date, ignore for status
        
        if qty < 5: # Arbitrary low stock threshold
            status_indicator += " (LOW STOCK!)"

        print(f"{name:<30} {qty:<5} {expires:<12} {location:<20}{status_indicator}")
    print("-------------------------")

def main():
    parser = argparse.ArgumentParser(description="Apocalypse Resource Tracker - Manage your vital supplies.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new item or increase quantity of an existing one.')
    add_parser.add_argument('name', type=str, help='Name of the item.')
    add_parser.add_argument('quantity', type=int, help='Quantity to add.')
    add_parser.add_argument('--expires', type=str, help='Expiration date (YYYY-MM-DD).')
    add_parser.add_argument('--location', type=str, help='Storage location.')

    # Consume command
    consume_parser = subparsers.add_parser('consume', help='Consume a quantity of an existing item.')
    consume_parser.add_argument('name', type=str, help='Name of the item.')
    consume_parser.add_argument('quantity', type=int, help='Quantity to consume.')

    # List command
    list_parser = subparsers.add_parser('list', help='List all items in inventory.')

    args = parser.parse_args()

    if args.command == 'add':
        add_item(args.name, args.quantity, args.expires, args.location)
    elif args.command == 'consume':
        consume_item(args.name, args.quantity)
    elif args.command == 'list':
        list_items()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
