import argparse
import csv
import sys
from typing import List, NamedTuple

class FoodItem(NamedTuple):
    name: str
    shelf_life_days: int
    calories_per_serving: int
    category: str

def parse_food_items(file_path: str) -> List[FoodItem]:
    """Parses a CSV file into a list of FoodItem objects."""
    items = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Skip header row
            next(reader, None)
            for i, row in enumerate(reader):
                if len(row) != 4:
                    print(f"Warning: Skipping malformed row {i+2} in {file_path}: {row}", file=sys.stderr)
                    continue
                try:
                    name = row[0]
                    shelf_life = int(row[1])
                    calories = int(row[2])
                    category = row[3]
                    items.append(FoodItem(name, shelf_life, calories, category))
                except ValueError as e:
                    print(f"Warning: Skipping row {i+2} due to data conversion error: {e} in row: {row}", file=sys.stderr)
                    continue
    except FileNotFoundError:
        print(f"Error: Input file '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)
    return items

def sort_food_items(items: List[FoodItem]) -> List[FoodItem]:
    """Sorts food items by shelf life (desc) then calories (desc)."""
    return sorted(items, key=lambda item: (item.shelf_life_days, item.calories_per_serving), reverse=True)

def print_items(items: List[FoodItem], output_file_path: str = None):
    """Prints sorted food items to stdout or a specified file."""
    output = []
    header = ["Item Name", "Shelf Life (days)", "Calories per serving", "Category"]
    
    if output_file_path:
        try:
            with open(output_file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([h.replace(' (days)', '').replace(' per serving', '') for h in header]) # Clean header for CSV
                for item in items:
                    writer.writerow([item.name, item.shelf_life_days, item.calories_per_serving, item.category])
            print(f"Sorted supplies written to '{output_file_path}'.")
        except Exception as e:
            print(f"Error writing to output file '{output_file_path}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        output.append("Sorted Supplies:")
        output.append("----------------")
        
        # Calculate max widths for pretty printing
        col_widths = [len(h) for h in header]
        for item in items:
            col_widths[0] = max(col_widths[0], len(item.name))
            col_widths[1] = max(col_widths[1], len(str(item.shelf_life_days)))
            col_widths[2] = max(col_widths[2], len(str(item.calories_per_serving)))
            col_widths[3] = max(col_widths[3], len(item.category))

        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(header))
        output.append(header_line)
        output.append("-" * len(header_line))

        for item in items:
            line = " | ".join([
                item.name.ljust(col_widths[0]),
                str(item.shelf_life_days).ljust(col_widths[1]),
                str(item.calories_per_serving).ljust(col_widths[2]),
                item.category.ljust(col_widths[3])
            ])
            output.append(line)
        for line in output:
            print(line)

def main():
    parser = argparse.ArgumentParser(
        description="Sorts apocalypse food supplies by shelf life and caloric density."
    )
    parser.add_argument("--input", required=True, help="Path to the input CSV file.")
    parser.add_argument("--output", help="Path to the output CSV file (optional). If not provided, output to stdout.")

    args = parser.parse_args()

    food_items = parse_food_items(args.input)
    if not food_items:
        print("No valid food items found to sort.", file=sys.stderr)
        sys.exit(2) # Exit code 2 for no-op (nothing to change/sort)

    sorted_items = sort_food_items(food_items)
    print_items(sorted_items, args.output)

if __name__ == "__main__":
    main()
