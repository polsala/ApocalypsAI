import argparse
import json
import os

class ResourceTracker:
    def __init__(self, initial_resources: dict = None):
        # Ensure all resource quantities are floats for consistent arithmetic
        self.resources = {k: float(v) for k, v in (initial_resources or {}).items()}

    def add_resource(self, resource_name: str, quantity: float) -> bool:
        if not isinstance(quantity, (int, float)) or quantity < 0:
            raise ValueError("Quantity must be a non-negative number.")
        self.resources[resource_name] = self.resources.get(resource_name, 0.0) + quantity
        return True

    def consume_resource(self, resource_name: str, quantity: float) -> bool:
        if not isinstance(quantity, (int, float)) or quantity < 0:
            raise ValueError("Quantity must be a non-negative number.")
        current_level = self.resources.get(resource_name, 0.0)
        if current_level < quantity:
            return False # Not enough resource
        self.resources[resource_name] -= quantity
        return True

    def get_resource_level(self, resource_name: str) -> float:
        return self.resources.get(resource_name, 0.0)

    def estimate_survival_days(self, daily_consumption: dict) -> dict:
        estimates = {}
        for resource, consumption_rate in daily_consumption.items():
            if not isinstance(consumption_rate, (int, float)) or consumption_rate < 0:
                raise ValueError(f"Daily consumption rate for '{resource}' must be a non-negative number.")

            current_level = self.resources.get(resource, 0.0)
            if consumption_rate == 0:
                estimates[resource] = float('inf') # Infinite days if no consumption
            else:
                estimates[resource] = current_level / consumption_rate
        return estimates

    def to_json(self) -> str:
        return json.dumps(self.resources, indent=4)

    @classmethod
    def from_json(cls, json_string: str):
        return cls(json.loads(json_string))


def main():
    parser = argparse.ArgumentParser(description="Rubble-Rouser's Resource Tracker: Manage your post-apocalyptic supplies.")
    parser.add_argument('--state-file', default='tracker_state.json', help='File to save/load tracker state. Defaults to tracker_state.json in the current directory.')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize tracker with resources. Overwrites existing state.')
    init_parser.add_argument('resources', nargs='*', help='Initial resources in key=value format (e.g., food=100 water=50)')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add resources to the tracker.')
    add_parser.add_argument('resources', nargs='+', help='Resources to add in key=value format (e.g., food=10 water=5)')

    # Consume command
    consume_parser = subparsers.add_parser('consume', help='Consume resources from the tracker.')
    consume_parser.add_argument('resources', nargs='+', help='Resources to consume in key=value format (e.g., food=5 water=3)')

    # Levels command
    levels_parser = subparsers.add_parser('levels', help='Show current resource levels.')

    # Estimate command
    estimate_parser = subparsers.add_parser('estimate', help='Estimate survival days based on daily consumption.')
    estimate_parser.add_argument('consumption', nargs='+', help='Daily consumption rates in key=value format (e.g., food=10 water=5)')

    args = parser.parse_args()

    tracker = ResourceTracker()
    if os.path.exists(args.state_file):
        with open(args.state_file, 'r') as f:
            try:
                tracker = ResourceTracker.from_json(f.read())
            except json.JSONDecodeError:
                print(f"Warning: Could not load state from {args.state_file}. File might be corrupted. Starting fresh.")
                tracker = ResourceTracker()
            except Exception as e:
                print(f"Error loading state from {args.state_file}: {e}. Starting fresh.")
                tracker = ResourceTracker()

    def parse_key_value_args(arg_list):
        parsed = {}
        for item in arg_list:
            if '=' in item:
                key, value = item.split('=', 1)
                try:
                    parsed[key] = float(value)
                except ValueError:
                    print(f"Error: Invalid quantity for '{key}'. Must be a number.")
                    exit(1)
            else:
                print(f"Error: Invalid format for '{item}'. Expected key=value.")
                exit(1)
        return parsed

    if args.command == 'init':
        initial_resources = parse_key_value_args(args.resources)
        tracker = ResourceTracker(initial_resources)
        print("Tracker initialized.")
    elif args.command == 'add':
        resources_to_add = parse_key_value_args(args.resources)
        for res, qty in resources_to_add.items():
            try:
                tracker.add_resource(res, qty)
                print(f"Added {qty:.2f} of {res}.")
            except ValueError as e:
                print(f"Error adding {res}: {e}")
                exit(1)
    elif args.command == 'consume':
        resources_to_consume = parse_key_value_args(args.resources)
        for res, qty in resources_to_consume.items():
            try:
                if tracker.consume_resource(res, qty):
                    print(f"Consumed {qty:.2f} of {res}.")
                else:
                    print(f"Warning: Not enough {res} to consume {qty:.2f}. Current: {tracker.get_resource_level(res):.2f}")
            except ValueError as e:
                print(f"Error consuming {res}: {e}")
                exit(1)
    elif args.command == 'levels':
        if not tracker.resources:
            print("No resources tracked yet.")
        else:
            print("Current Resource Levels:")
            for res, level in sorted(tracker.resources.items()):
                print(f"  {res}: {level:.2f}")
    elif args.command == 'estimate':
        daily_consumption = parse_key_value_args(args.consumption)
        try:
            estimates = tracker.estimate_survival_days(daily_consumption)
            print("Survival Estimates (Days Remaining):")
            for res, days in sorted(estimates.items()):
                if days == float('inf'):
                    print(f"  {res}: Indefinite (no consumption or infinite supply)")
                else:
                    print(f"  {res}: {days:.2f} days")
        except ValueError as e:
            print(f"Error estimating survival days: {e}")
            exit(1)
    else:
        parser.print_help()

    # Save state after any operation that modifies it
    if args.command in ['init', 'add', 'consume']:
        with open(args.state_file, 'w') as f:
            f.write(tracker.to_json())

if __name__ == '__main__':
    main()
