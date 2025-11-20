import json
import os
import argparse

class ResourceTracker:
    def __init__(self, data_file="resources.json"):
        self.data_file = data_file
        self.resources = self._load_resources()

    def _load_resources(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON from {self.data_file}. Starting with empty resources.")
                    return {}
        return {}

    def _save_resources(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.resources, f, indent=4)

    def add_resource(self, name: str, quantity: int, threshold: int = 0):
        if not isinstance(name, str) or not name:
            raise ValueError("Resource name must be a non-empty string.")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")
        if not isinstance(threshold, int) or threshold < 0:
            raise ValueError("Threshold must be a non-negative integer.")

        if name in self.resources:
            print(f"Resource '{name}' already exists. Updating quantity and threshold.")
        self.resources[name] = {"quantity": quantity, "threshold": threshold}
        self._save_resources()
        return True

    def update_quantity(self, name: str, change: int):
        if name not in self.resources:
            print(f"Resource '{name}' not found. Please add it first.")
            return False
        
        new_quantity = self.resources[name]["quantity"] + change
        if new_quantity < 0:
            print(f"Warning: Quantity for '{name}' cannot go below zero. Setting to 0.")
            self.resources[name]["quantity"] = 0
        else:
            self.resources[name]["quantity"] = new_quantity
        self._save_resources()
        return True

    def set_threshold(self, name: str, threshold: int):
        if name not in self.resources:
            print(f"Resource '{name}' not found. Please add it first.")
            return False
        if not isinstance(threshold, int) or threshold < 0:
            raise ValueError("Threshold must be a non-negative integer.")
        self.resources[name]["threshold"] = threshold
        self._save_resources()
        return True

    def get_status(self, name: str):
        if name not in self.resources:
            return "Not Found"
        
        resource = self.resources[name]
        if resource["quantity"] <= resource["threshold"]:
            return "LOW"
        return "OK"

    def list_resources(self):
        if not self.resources:
            return "No resources tracked yet."
        
        output = []
        for name, data in self.resources.items():
            status = self.get_status(name)
            output.append(f"- {name}: {data['quantity']} (Threshold: {data['threshold']}) - Status: {status}")
        return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description="Rubble-Rouser Resource Tracker: Manage your essential survival resources."
    )
    parser.add_argument("--data-file", default="resources.json", help="Path to the resource data file.")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new resource or update an existing one.")
    add_parser.add_argument("name", type=str, help="Name of the resource.")
    add_parser.add_argument("quantity", type=int, help="Initial quantity of the resource.")
    add_parser.add_argument("--threshold", type=int, default=0, help="Low-stock threshold for the resource.")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update the quantity of an existing resource.")
    update_parser.add_argument("name", type=str, help="Name of the resource.")
    update_parser.add_argument("change", type=int, help="Change in quantity (positive for add, negative for remove).")

    # Set threshold command
    set_threshold_parser = subparsers.add_parser("set-threshold", help="Set the low-stock threshold for a resource.")
    set_threshold_parser.add_argument("name", type=str, help="Name of the resource.")
    set_threshold_parser.add_argument("threshold", type=int, help="New low-stock threshold.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tracked resources and their statuses.")

    args = parser.parse_args()

    tracker = ResourceTracker(args.data_file)

    if args.command == "add":
        tracker.add_resource(args.name, args.quantity, args.threshold)
        print(f"Resource '{args.name}' added/updated.")
    elif args.command == "update":
        if tracker.update_quantity(args.name, args.change):
            print(f"Quantity for '{args.name}' updated.")
    elif args.command == "set-threshold":
        if tracker.set_threshold(args.name, args.threshold):
            print(f"Threshold for '{args.name}' updated.")
    elif args.command == "list":
        print("--- Current Resources ---")
        print(tracker.list_resources())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
