import yaml
import argparse
from datetime import date, timedelta
import sys

def load_config(config_path):
    """Loads the snack inventory from a YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{config_path}'", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{config_path}': {e}", file=sys.stderr)
        sys.exit(1)

def parse_item(item_data):
    """Parses a single item's data, converting expiry_date to a date object."""
    try:
        name = item_data['name']
        quantity = int(item_data['quantity'])
        expiry_str = item_data['expiry_date']
        expiry_date = date.fromisoformat(expiry_str)
        return {'name': name, 'quantity': quantity, 'expiry_date': expiry_date}
    except KeyError as e:
        raise ValueError(f"Missing key in item data: {e}")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid value in item data: {e}")

def generate_report(inventory, warning_days, current_date=None):
    """Generates a formatted report of the snack inventory."""
    if current_date is None:
        current_date = date.today()

    all_parsed_items = []
    for item_data in inventory.get('items', []):
        try:
            item = parse_item(item_data)
            all_parsed_items.append(item)
        except ValueError as e:
            print(f"Warning: Skipping invalid item entry: {e}", file=sys.stderr)
            continue

    expired_items = []
    expiring_soon_items = []
    healthy_items = []

    for item in all_parsed_items:
        days_until_expiry = (item['expiry_date'] - current_date).days

        if days_until_expiry < 0:
            expired_items.append((item, abs(days_until_expiry)))
        elif days_until_expiry <= warning_days:
            expiring_soon_items.append((item, days_until_expiry))
        else:
            healthy_items.append((item, days_until_expiry))

    report_lines = []
    report_lines.append(f"Apocalypse Snack Stash Report (Today: {current_date.isoformat()})")
    report_lines.append("=" * len(report_lines[0]))
    report_lines.append("")

    def format_item_list(title, items, days_label):
        report_lines.append(f"--- {title} ({len(items)}) ---")
        if not items:
            report_lines.append("No items in this category.")
        else:
            for item, days in sorted(items, key=lambda x: x[1]):
                report_lines.append(f"- {item['name']} ({item['quantity']} units) - {days_label} {days} days ({item['expiry_date'].isoformat()})")
        report_lines.append("")

    format_item_list("Expired Items", expired_items, "Expired")
    format_item_list(f"Expiring Soon (< {warning_days} days)", expiring_soon_items, "Expires in")
    format_item_list("Healthy Stash", healthy_items, "Expires in")

    total_unique_items = len(all_parsed_items)
    total_units = sum(item['quantity'] for item in all_parsed_items)

    report_lines.append("--- Inventory Summary ---")
    report_lines.append(f"Total unique items: {total_unique_items}")
    report_lines.append(f"Total units: {total_units}")

    return "\n".join(report_lines)

def main():
    parser = argparse.ArgumentParser(description="Manage your apocalypse snack stash.")
    parser.add_argument('--config', default='snacks.yml', help='Path to the YAML configuration file.')
    parser.add_argument('--warning-days', type=int, default=30, help='Number of days before expiry to flag an item as "expiring soon".')
    args = parser.parse_args()

    inventory = load_config(args.config)
    report = generate_report(inventory, args.warning_days)
    print(report)

if __name__ == '__main__':
    main()
