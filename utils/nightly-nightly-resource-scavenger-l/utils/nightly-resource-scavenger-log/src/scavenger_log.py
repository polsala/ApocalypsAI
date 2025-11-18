import argparse
import json
import os
from collections import defaultdict

class ScavengerLog:
    def __init__(self, data_file='scavenger_log.json'):
        self.data_file = data_file
        self.log = self._load_log()

    def _load_log(self):
        if not os.path.exists(self.data_file):
            return defaultdict(lambda: defaultdict(int))
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                log = defaultdict(lambda: defaultdict(int))
                for loc, items in data.items():
                    for item, qty in items.items():
                        log[loc][item] = qty
                return log
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {self.data_file}. Starting with an empty log.")
            return defaultdict(lambda: defaultdict(int))
        except Exception as e:
            print(f"Error loading {self.data_file}: {e}. Starting with an empty log.")
            return defaultdict(lambda: defaultdict(int))

    def _save_log(self):
        # Convert defaultdicts back to regular dicts for JSON serialization
        serializable_log = {loc: dict(items) for loc, items in self.log.items()}
        with open(self.data_file, 'w') as f:
            json.dump(serializable_log, f, indent=4)

    def add_resource(self, item: str, quantity: int, location: str):
        if quantity <= 0:
            print("Quantity must be positive.")
            return
        self.log[location][item] += quantity
        self._save_log()
        print(f"Added {quantity}x {item} to {location}. Total: {self.log[location][item]}")

    def remove_resource(self, item: str, quantity: int, location: str):
        if quantity <= 0:
            print("Quantity must be positive.")
            return
        if item not in self.log[location] or self.log[location][item] < quantity:
            print(f"Not enough {item} in {location} to remove {quantity}. Current: {self.log[location].get(item, 0)}")
            return
        self.log[location][item] -= quantity
        if self.log[location][item] == 0:
            del self.log[location][item]
            if not self.log[location]: # If location is empty, remove it
                del self.log[location]
        self._save_log()
        print(f"Removed {quantity}x {item} from {location}. Remaining: {self.log[location].get(item, 0)}")

    def list_resources(self, location: str = None):
        if not self.log:
            print("The scavenger log is empty.")
            return

        if location:
            if location in self.log:
                print(f"\nResources in {location}:")
                for item, quantity in sorted(self.log[location].items()):
                    print(f"  - {item}: {quantity}")
            else:
                print(f"No resources found in location: {location}")
        else:
            print("\nAll Scavenged Resources:")
            for loc, items in sorted(self.log.items()):
                print(f"\nLocation: {loc}")
                for item, quantity in sorted(items.items()):
                    print(f"  - {item}: {quantity}")

def main():
    parser = argparse.ArgumentParser(description="Manage your scavenged resources.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a resource to a location.')
    add_parser.add_argument('--item', required=True, help='Name of the resource.')
    add_parser.add_argument('--quantity', type=int, required=True, help='Quantity to add.')
    add_parser.add_argument('--location', required=True, help='Location where the resource is stored.')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a resource from a location.')
    remove_parser.add_argument('--item', required=True, help='Name of the resource.')
    remove_parser.add_argument('--quantity', type=int, required=True, help='Quantity to remove.')
    remove_parser.add_argument('--location', required=True, help='Location from which to remove the resource.')

    # List command
    list_parser = subparsers.add_parser('list', help='List all or specific resources.')
    list_parser.add_argument('--location', help='(Optional) List resources only for a specific location.')

    args = parser.parse_args()

    # Determine the data file path relative to the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, 'scavenger_log.json')

    log_manager = ScavengerLog(data_file=data_file_path)

    if args.command == 'add':
        log_manager.add_resource(args.item, args.quantity, args.location)
    elif args.command == 'remove':
        log_manager.remove_resource(args.item, args.quantity, args.location)
    elif args.command == 'list':
        log_manager.list_resources(args.location)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
