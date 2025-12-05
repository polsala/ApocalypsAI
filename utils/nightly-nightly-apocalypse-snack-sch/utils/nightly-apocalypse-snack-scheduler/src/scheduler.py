import argparse
import yaml
from datetime import date, timedelta
import sys

def load_snacks(config_path):
    """Loads snack data from a YAML configuration file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{config_path}'", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{config_path}': {e}", file=sys.stderr)
        sys.exit(1)

def get_expiry_status(snack, today, warning_days):
    """Calculates the expiry status for a single snack."""
    try:
        expiry_date_str = snack['expiry_date']
        expiry_date = date.fromisoformat(expiry_date_str)
    except (KeyError, ValueError):
        return {
            'name': snack.get('name', 'Unknown Snack'),
            'quantity': snack.get('quantity', 'N/A'),
            'status': 'Invalid Date',
            'days_left': None,
            'color': 'red'
        }

    days_left = (expiry_date - today).days

    if days_left < 0:
        status = 'EXPIRED'
        color = 'red'
    elif days_left <= warning_days:
        status = 'Expiring Soon'
        color = 'yellow'
    else:
        status = 'OK'
        color = 'green'
    
    return {
        'name': snack['name'],
        'quantity': snack['quantity'],
        'status': status,
        'days_left': days_left,
        'color': color
    }

def print_report(statuses):
    """Prints a formatted report of snack expiry statuses."""
    print("\n--- Apocalypse Snack Inventory Report ---")
    print(f"Report Date: {date.today().isoformat()}")
    print("-" * 40)

    if not statuses:
        print("No snacks found in inventory.")
        return

    # Sort by days_left, expired first, then expiring soonest
    sorted_statuses = sorted(statuses, key=lambda x: x['days_left'] if x['days_left'] is not None else float('inf'))

    for status in sorted_statuses:
        name = status['name']
        quantity = status['quantity']
        days_left = status['days_left']
        status_text = status['status']
        color = status['color'] # Placeholder for future color output (e.g., with rich)

        if days_left is None:
            print(f"[{status_text}] {name} (Qty: {quantity}) - Invalid expiry date format.")
        elif days_left < 0:
            print(f"[{status_text}] {name} (Qty: {quantity}) - Expired {abs(days_left)} days ago!")
        elif days_left <= 0: # Expiring today
            print(f"[{status_text}] {name} (Qty: {quantity}) - Expiring TODAY!")
        elif days_left <= 30: # Special highlight for very soon
            print(f"[{status_text}] {name} (Qty: {quantity}) - {days_left} days left! ACT NOW!")
        elif status_text == 'Expiring Soon':
            print(f"[{status_text}] {name} (Qty: {quantity}) - {days_left} days left.")
        else:
            print(f"[{status_text}] {name} (Qty: {quantity}) - {days_left} days left.")
    
    print("-" * 40)
    print("Remember to rotate your snacks!")

def main():
    parser = argparse.ArgumentParser(
        description="Track and remind about expiring 'apocalypse snacks'."
    )
    parser.add_argument(
        "--config",
        default="snacks.yaml",
        help="Path to the YAML configuration file (default: snacks.yaml)"
    )
    parser.add_argument(
        "--warning-days",
        type=int,
        default=90,
        help="Number of days before expiry to issue a 'Expiring Soon' warning (default: 90)"
    )
    args = parser.parse_args()

    snacks = load_snacks(args.config)
    
    today = date.today()
    statuses = [get_expiry_status(snack, today, args.warning_days) for snack in snacks]
    
    print_report(statuses)

if __name__ == "__main__":
    main()
