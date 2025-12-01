import csv
import sys
from typing import List, Dict, Any

def calculate_priority_score(item: Dict[str, Any]) -> float:
    """
    Calculates the consumption priority score for a given food item.
    Lower score indicates higher priority.
    Formula: (shelf_life_days * 1) - (calories_per_serving * servings * 0.01)
    """
    try:
        shelf_life_days = int(item['shelf_life_days'])
        calories_per_serving = int(item['calories_per_serving'])
        servings = int(item['servings'])
    except (ValueError, KeyError) as e:
        print(f"Error parsing item data for '{item.get('item_name', 'Unknown')}': {e}", file=sys.stderr)
        return float('inf') # Assign lowest priority if data is malformed

    total_calories = calories_per_serving * servings
    # Shorter shelf life -> lower score (higher priority)
    # More total calories -> lower score (higher priority)
    score = (shelf_life_days * 1.0) - (total_calories * 0.01)
    return score

def load_inventory(filepath: str) -> List[Dict[str, Any]]:
    """Loads inventory from a CSV file."""
    inventory = []
    try:
        with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                inventory.append(row)
    except FileNotFoundError:
        print(f"Error: Inventory file '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)
    return inventory

def sort_inventory(inventory: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sorts the inventory by priority score."""
    for item in inventory:
        item['priority_score'] = calculate_priority_score(item)
        item['total_calories'] = int(item.get('calories_per_serving', 0)) * int(item.get('servings', 0))

    # Sort by priority_score (ascending)
    return sorted(inventory, key=lambda x: x['priority_score'])

def print_sorted_inventory(sorted_inventory: List[Dict[str, Any]]):
    """Prints the sorted inventory in a formatted table."""
    if not sorted_inventory:
        print("No items to display.")
        return

    print("\nApocalypse Snack Sorter - Prioritized Consumption List\n")

    headers = ["Item Name", "Shelf Life (Days)", "Calories (Total)", "Servings", "Priority Score"]
    # Determine max width for each column
    col_widths = {header: len(header) for header in headers}
    for item in sorted_inventory:
        col_widths["Item Name"] = max(col_widths["Item Name"], len(item.get('item_name', 'N/A')))
        col_widths["Shelf Life (Days)"] = max(col_widths["Shelf Life (Days)"], len(str(item.get('shelf_life_days', 'N/A'))))
        col_widths["Calories (Total)"] = max(col_widths["Calories (Total)"], len(str(item.get('total_calories', 'N/A'))))
        col_widths["Servings"] = max(col_widths["Servings"], len(str(item.get('servings', 'N/A'))))
        col_widths["Priority Score"] = max(col_widths["Priority Score"], len(f"{item.get('priority_score', 0.0):.2f}"))

    # Print header
    header_line = "+-" + "-+-".join(["-" * col_widths[h] for h in headers]) + "-+"
    print(header_line)
    print("| " + " | ".join([h.ljust(col_widths[h]) for h in headers]) + " |")
    print(header_line)

    # Print items
    for item in sorted_inventory:
        item_name = item.get('item_name', 'N/A').ljust(col_widths["Item Name"])
        shelf_life = str(item.get('shelf_life_days', 'N/A')).ljust(col_widths["Shelf Life (Days)"])
        total_calories = str(item.get('total_calories', 'N/A')).ljust(col_widths["Calories (Total)"])
        servings = str(item.get('servings', 'N/A')).ljust(col_widths["Servings"])
        priority_score = f"{item.get('priority_score', 0.0):.2f}".ljust(col_widths["Priority Score"])
        print(f"| {item_name} | {shelf_life} | {total_calories} | {servings} | {priority_score} |")
    print(header_line)
    print("\n*Lower Priority Score indicates higher consumption priority.*")


def main():
    if len(sys.argv) < 2:
        print("Usage: python sorter.py <path_to_inventory.csv>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    inventory = load_inventory(filepath)
    if not inventory:
        print("No valid items found in inventory.", file=sys.stderr)
        sys.exit(0)

    sorted_inventory = sort_inventory(inventory)
    print_sorted_inventory(sorted_inventory)

if __name__ == "__main__":
    main()
