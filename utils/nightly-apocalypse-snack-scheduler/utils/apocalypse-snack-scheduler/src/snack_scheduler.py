import json
import os
from datetime import date, timedelta

CONFIG_FILE = 'snacks.json'

def load_snacks(file_path):
    """Loads snack data from a JSON file."""
    if not os.path.exists(file_path):
        print(f"Error: Configuration file '{file_path}' not found.")
        return None
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{file_path}'.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading '{file_path}': {e}")
        return None

def calculate_next_check(last_checked_str, frequency_days):
    """Calculates the next check date."""
    try:
        last_checked = date.fromisoformat(last_checked_str)
        return last_checked + timedelta(days=frequency_days)
    except ValueError:
        return None # Invalid date format

def main():
    today = date.today()
    script_dir = os.path.dirname(__file__)
    config_path = os.path.join(script_dir, CONFIG_FILE)

    snacks = load_snacks(config_path)

    if snacks is None:
        return

    print(f"Apocalypse Snack Scheduler Report (Today: {today.isoformat()})")
    print("---------------------------------------------------")

    due_items = []

    for item in snacks:
        name = item.get('name', 'Unknown Item')
        last_checked_str = item.get('last_checked')
        check_frequency_days = item.get('check_frequency_days')

        if not all([last_checked_str, isinstance(check_frequency_days, int)]):
            print(f"Warning: Skipping item '{name}' due to missing or invalid 'last_checked' or 'check_frequency_days'.")
            continue

        next_check = calculate_next_check(last_checked_str, check_frequency_days)

        if next_check is None:
            print(f"Warning: Skipping item '{name}' due to invalid 'last_checked' date format: '{last_checked_str}'.")
            continue

        if next_check <= today:
            due_items.append({
                'name': name,
                'next_check': next_check,
                'last_checked': last_checked_str
            })

    if due_items:
        print("\nItems due for checking:\n")
        for item in due_items:
            status = "Overdue" if item['next_check'] < today else "Due today"
            print(f"- {item['name']} - {status} since {item['next_check'].isoformat()} (Last checked: {item['last_checked']})")
    else:
        print("\nNo items are due for checking. All clear for now!")

    print("\nStay vigilant!")

if __name__ == '__main__':
    main()
