import argparse
import json
import os
from datetime import datetime, timedelta

DATA_FILE = 'resources.json'
DATE_FORMAT = '%Y-%m-%d'

class ResourceTracker:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.resources = self._load_resources()

    def _load_resources(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode {self.data_file}. Starting with empty resources.")
                    return {}
        return {}

    def _save_resources(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.resources, f, indent=4)

    def add_resource(self, name, quantity, expiry_date_str=None, notes=""):
        name = name.lower()
        if name in self.resources:
            print(f"Resource '{name}' already exists. Use 'update' to modify.")
            return False

        try:
            expiry_date = datetime.strptime(expiry_date_str, DATE_FORMAT).date() if expiry_date_str else None
        except ValueError:
            print(f"Error: Invalid expiry date format. Use YYYY-MM-DD.")
            return False

        self.resources[name] = {
            'name': name,
            'quantity': quantity,
            'expiry_date': expiry_date.strftime(DATE_FORMAT) if expiry_date else None,
            'notes': notes
        }
        self._save_resources()
        print(f"Added resource: {name} (Qty: {quantity})")
        return True

    def update_resource(self, name, quantity=None, expiry_date_str=None, notes=None):
        name = name.lower()
        if name not in self.resources:
            print(f"Resource '{name}' not found.")
            return False

        if quantity is not None:
            self.resources[name]['quantity'] = quantity
        
        if expiry_date_str is not None:
            try:
                expiry_date = datetime.strptime(expiry_date_str, DATE_FORMAT).date()
                self.resources[name]['expiry_date'] = expiry_date.strftime(DATE_FORMAT)
            except ValueError:
                print(f"Error: Invalid expiry date format. Use YYYY-MM-DD.")
                return False

        if notes is not None:
            self.resources[name]['notes'] = notes

        self._save_resources()
        print(f"Updated resource: {name}")
        return True

    def remove_resource(self, name):
        name = name.lower()
        if name in self.resources:
            del self.resources[name]
            self._save_resources()
            print(f"Removed resource: {name}")
            return True
        print(f"Resource '{name}' not found.")
        return False

    def list_resources(self):
        if not self.resources:
            print("No resources tracked yet.")
            return []
        
        print("\n--- All Tracked Resources ---")
        sorted_resources = sorted(self.resources.values(), key=lambda x: x['name'])
        for res in sorted_resources:
            expiry = f"Expires: {res['expiry_date']}" if res['expiry_date'] else "No Expiry"
            notes = f" ({res['notes']})" if res['notes'] else ""
            print(f"- {res['name'].title()}: Qty {res['quantity']}, {expiry}{notes}")
        print("-----------------------------\n")
        return sorted_resources

    def get_expiring_resources(self, days=30):
        expiring = []
        today = datetime.now().date()
        threshold_date = today + timedelta(days=days)

        print(f"\n--- Resources Expiring within {days} Days ---")
        found = False
        for res_name, res_data in self.resources.items():
            if res_data['expiry_date']:
                expiry_date = datetime.strptime(res_data['expiry_date'], DATE_FORMAT).date()
                if today <= expiry_date <= threshold_date:
                    print(f"- {res_data['name'].title()}: Qty {res_data['quantity']}, Expires: {res_data['expiry_date']}")
                    expiring.append(res_data)
                    found = True
        if not found:
            print("No resources expiring soon.")
        print("-------------------------------------------\n")
        return expiring

    def get_low_stock_resources(self, threshold=5):
        low_stock = []
        print(f"\n--- Resources Below Stock Threshold ({threshold}) ---")
        found = False
        for res_name, res_data in self.resources.items():
            if res_data['quantity'] < threshold:
                print(f"- {res_data['name'].title()}: Qty {res_data['quantity']}")
                low_stock.append(res_data)
                found = True
        if not found:
            print("No resources are currently low on stock.")
        print("-----------------------------------------------\n")
        return low_stock

def main():
    parser = argparse.ArgumentParser(description="Apocalypse Resource Tracker - Keep tabs on your essential supplies.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new resource')
    add_parser.add_argument('--name', required=True, help='Name of the resource')
    add_parser.add_argument('--qty', type=int, required=True, help='Quantity of the resource')
    add_parser.add_argument('--expiry', help='Expiry date (YYYY-MM-DD)')
    add_parser.add_argument('--notes', default="", help='Additional notes for the resource')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update an existing resource')
    update_parser.add_argument('--name', required=True, help='Name of the resource to update')
    update_parser.add_argument('--qty', type=int, help='New quantity')
    update_parser.add_argument('--expiry', help='New expiry date (YYYY-MM-DD)')
    update_parser.add_argument('--notes', help='New notes')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a resource')
    remove_parser.add_argument('--name', required=True, help='Name of the resource to remove')

    # List command
    list_parser = subparsers.add_parser('list', help='List all tracked resources')

    # Expiring command
    expiring_parser = subparsers.add_parser('expiring', help='Show resources expiring soon')
    expiring_parser.add_argument('--days', type=int, default=30, help='Number of days to check for expiry (default: 30)')

    # Low-stock command
    low_stock_parser = subparsers.add_parser('low-stock', help='Show resources with low stock')
    low_stock_parser.add_argument('--threshold', type=int, default=5, help='Stock quantity threshold (default: 5)')

    args = parser.parse_args()
    tracker = ResourceTracker()

    if args.command == 'add':
        tracker.add_resource(args.name, args.qty, args.expiry, args.notes)
    elif args.command == 'update':
        tracker.update_resource(args.name, args.qty, args.expiry, args.notes)
    elif args.command == 'remove':
        tracker.remove_resource(args.name)
    elif args.command == 'list':
        tracker.list_resources()
    elif args.command == 'expiring':
        tracker.get_expiring_resources(args.days)
    elif args.command == 'low-stock':
        tracker.get_low_stock_resources(args.threshold)
    elif args.command is None:
        parser.print_help()

if __name__ == '__main__':
    main()
