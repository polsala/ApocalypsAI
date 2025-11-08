import argparse
import csv
from datetime import datetime
import sys

def load_inventory(filepath):
    """Loads inventory from a CSV file."""
    inventory = []
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if len(row) != 4:
                    print(f"Warning: Skipping malformed line {i+1} in {filepath}: {row}", file=sys.stderr)
                    continue
                try:
                    item_name, exp_date_str, category, quantity_str = row
                    exp_date = datetime.strptime(exp_date_str, '%Y-%m-%d').date()
                    quantity = int(quantity_str)
                    inventory.append({
                        'item_name': item_name.strip(),
                        'expiration_date': exp_date,
                        'category': category.strip(),
                        'quantity': quantity
                    })
                except ValueError as e:
                    print(f"Warning: Skipping line {i+1} due to data parsing error: {e} in row {row}", file=sys.stderr)
                    continue
    except FileNotFoundError:
        print(f"Error: Inventory file not found at '{filepath}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error loading inventory: {e}", file=sys.stderr)
        sys.exit(1)
    return inventory

def sort_inventory(inventory, sort_key):
    """Sorts the inventory based on the specified key."""
    if sort_key == 'expiration':
        return sorted(inventory, key=lambda x: x['expiration_date'])
    elif sort_key == 'category':
        return sorted(inventory, key=lambda x: (x['category'], x['item_name']))
    else:
        raise ValueError("Invalid sort_key. Must be 'expiration' or 'category'.")

def display_inventory(inventory, sort_key):
    """Prints the inventory in a formatted table."""
    print(f"---\n--- Survival Inventory (Sorted by {sort_key.capitalize()}) ---\n")
    if not inventory:
        print("No items in inventory.")
        return

    headers = ["Item Name", "Expiration", "Category", "Quantity"]
    # Determine max width for each column
    col_widths = {
        'item_name': max(len(item['item_name']) for item in inventory + [{'item_name': headers[0]}]),
        'expiration_date': max(len(str(item['expiration_date'])) for item in inventory + [{'expiration_date': headers[1]}]),
        'category': max(len(item['category']) for item in inventory + [{'category': headers[2]}]),
        'quantity': max(len(str(item['quantity'])) for item in inventory + [{'quantity': headers[3]}]),
    }

    # Adjust for header length if header is longer than any item
    col_widths['item_name'] = max(col_widths['item_name'], len(headers[0]))
    col_widths['expiration_date'] = max(col_widths['expiration_date'], len(headers[1]))
    col_widths['category'] = max(col_widths['category'], len(headers[2]))
    col_widths['quantity'] = max(col_widths['quantity'], len(headers[3]))

    # Print header
    print(f"{headers[0]:<{col_widths['item_name']}}}  "
          f"{headers[1]:<{col_widths['expiration_date']}}}  "
          f"{headers[2]:<{col_widths['category']]}}}  "
          f"{headers[3]:<{col_widths['quantity']}]}")
    print("-" * (sum(col_widths.values()) + 6)) # 6 for the spaces between columns

    # Print items
    for item in inventory:
        print(f"{item['item_name']:<{col_widths['item_name']}}}  "
              f"{str(item['expiration_date']):<{col_widths['expiration_date']}}}  "
              f"{item['category']:<{col_widths['category']]}}}  "
              f"{item['quantity']:<{col_widths['quantity']}]}")

def main():
    parser = argparse.ArgumentParser(description="Survival Snack Sorter: Organize your provisions.")
    parser.add_argument('--file', required=True, help="Path to the inventory CSV file.")
    parser.add_argument('--sort-by', choices=['expiration', 'category'], default='expiration',
                        help="Sort inventory by 'expiration' date or 'category'.")
    args = parser.parse_args()

    inventory = load_inventory(args.file)
    if inventory:
        sorted_items = sort_inventory(inventory, args.sort_by)
        display_inventory(sorted_items, args.sort_by)

if __name__ == '__main__':
    main()
