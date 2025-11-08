import argparse
import json
import os
from typing import Dict, Any

DATA_FILE = os.path.join(os.path.dirname(__file__), 'resources.json')

class ResourceTracker:
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.resources: Dict[str, Dict[str, Any]] = self._load_resources()

    def _load_resources(self) -> Dict[str, Dict[str, Any]]:
        if not os.path.exists(self.data_file):
            return {}
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {self.data_file}. Starting with empty resources.")
            return {}

    def _save_resources(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.resources, f, indent=4)

    def add_resource(self, name: str, quantity: int, threshold: int = 0):
        name = name.lower()
        if name in self.resources:
            print(f"Resource '{name}' already exists. Use 'replenish' or 'set-threshold' to update.")
            return
        self.resources[name] = {"quantity": quantity, "threshold": threshold}
        self._save_resources()
        print(f"Added resource '{name}' with quantity {quantity} and threshold {threshold}.")

    def remove_resource(self, name: str):
        name = name.lower()
        if name not in self.resources:
            print(f"Resource '{name}' not found.")
            return
        del self.resources[name]
        self._save_resources()
        print(f"Removed resource '{name}'.")

    def update_quantity(self, name: str, change: int, operation: str):
        name = name.lower()
        if name not in self.resources:
            print(f"Resource '{name}' not found. Please add it first.")
            return

        current_quantity = self.resources[name]["quantity"]
        if operation == "replenish":
            new_quantity = current_quantity + change
            print(f"Replenished {change} of '{name}'. New quantity: {new_quantity}.")
        elif operation == "consume":
            if current_quantity < change:
                print(f"Warning: Trying to consume {change} of '{name}', but only {current_quantity} available.")
                new_quantity = 0
            else:
                new_quantity = current_quantity - change
            print(f"Consumed {change} of '{name}'. New quantity: {new_quantity}.")
        else:
            raise ValueError("Invalid operation. Must be 'replenish' or 'consume'.")

        self.resources[name]["quantity"] = new_quantity
        self._save_resources()
        self._check_threshold(name)

    def set_threshold(self, name: str, threshold: int):
        name = name.lower()
        if name not in self.resources:
            print(f"Resource '{name}' not found. Please add it first.")
            return
        self.resources[name]["threshold"] = threshold
        self._save_resources()
        print(f"Set threshold for '{name}' to {threshold}.")
        self._check_threshold(name)

    def get_status(self):
        if not self.resources:
            print("No resources tracked yet. Add some with 'add' command!")
            return

        print("\n--- Wasteland Resource Status ---")
        for name, data in self.resources.items():
            quantity = data["quantity"]
            threshold = data["threshold"]
            status_line = f"- {name.capitalize()}: {quantity} (Threshold: {threshold})"
            if quantity <= threshold:
                status_line += " [CRITICAL!]"
            print(status_line)
        print("---------------------------------\n")

    def _check_threshold(self, name: str):
        name = name.lower()
        if name in self.resources:
            quantity = self.resources[name]["quantity"]
            threshold = self.resources[name]["threshold"]
            if quantity <= threshold:
                print(f"ALERT: '{name.capitalize()}' quantity ({quantity}) is at or below its critical threshold ({threshold})!")

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Resource Tracker: Manage your post-apocalyptic supplies.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status command
    status_parser = subparsers.add_parser("status", help="Display current resource status and alerts.")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new resource.")
    add_parser.add_argument("--name", required=True, help="Name of the resource.")
    add_parser.add_argument("--quantity", type=int, required=True, help="Initial quantity of the resource.")
    add_parser.add_argument("--threshold", type=int, default=0, help="Critical threshold for the resource (default: 0).")

    # Consume command
    consume_parser = subparsers.add_parser("consume", help="Consume a quantity of an existing resource.")
    consume_parser.add_argument("--name", required=True, help="Name of the resource to consume.")
    consume_parser.add_argument("--quantity", type=int, required=True, help="Quantity to consume.")

    # Replenish command
    replenish_parser = subparsers.add_parser("replenish", help="Replenish a quantity of an existing resource.")
    replenish_parser.add_argument("--name", required=True, help="Name of the resource to replenish.")
    replenish_parser.add_argument("--quantity", type=int, required=True, help="Quantity to replenish.")

    # Set Threshold command
    set_threshold_parser = subparsers.add_parser("set-threshold", help="Set or update the critical threshold for a resource.")
    set_threshold_parser.add_argument("--name", required=True, help="Name of the resource.")
    set_threshold_parser.add_argument("--threshold", type=int, required=True, help="New critical threshold.")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a resource entirely.")
    remove_parser.add_argument("--name", required=True, help="Name of the resource to remove.")

    args = parser.parse_args()
    tracker = ResourceTracker()

    if args.command == "status":
        tracker.get_status()
    elif args.command == "add":
        tracker.add_resource(args.name, args.quantity, args.threshold)
    elif args.command == "consume":
        tracker.update_quantity(args.name, args.quantity, "consume")
    elif args.command == "replenish":
        tracker.update_quantity(args.name, args.quantity, "replenish")
    elif args.command == "set-threshold":
        tracker.set_threshold(args.name, args.threshold)
    elif args.command == "remove":
        tracker.remove_resource(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
