import json
import argparse
import sys

def load_snacks(filepath: str) -> list[dict]:
    """Loads snack data from a JSON file with validation."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            snacks = json.load(f)
        
        if not isinstance(snacks, list):
            raise ValueError("Snack data must be a list of objects.")
        
        for snack in snacks:
            required_keys = ['name', 'calories_per_serving', 'shelf_life_days', 'morale_boost']
            if not all(k in snack for k in required_keys):
                missing_keys = [k for k in required_keys if k not in snack]
                raise ValueError(f"Snack missing required key(s): {', '.join(missing_keys)} in {snack}")
            
            if not isinstance(snack['name'], str) or \
               not isinstance(snack['calories_per_serving'], int) or \
               not isinstance(snack['shelf_life_days'], int) or \
               not isinstance(snack['morale_boost'], int):
                raise ValueError(f"Snack has invalid data types for one or more fields: {snack}")
            
            if not (1 <= snack['morale_boost'] <= 5):
                raise ValueError(f"Morale boost must be between 1 and 5: {snack}")
                
        return snacks
    except FileNotFoundError:
        print(f"Error: Inventory file not found at '{filepath}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filepath}'", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid snack data in '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)

def sort_by_shelf_life(snacks: list[dict]) -> list[dict]:
    """Sorts snacks by remaining shelf life (descending)."""
    return sorted(snacks, key=lambda s: s['shelf_life_days'], reverse=True)

def sort_by_calories(snacks: list[dict]) -> list[dict]:
    """Sorts snacks by caloric density (descending)."""
    return sorted(snacks, key=lambda s: s['calories_per_serving'], reverse=True)

def find_high_morale_boosters(snacks: list[dict], count: int = 3) -> list[dict]:
    """Finds the top 'count' snacks with the highest morale boost."""
    sorted_by_morale = sorted(snacks, key=lambda s: s['morale_boost'], reverse=True)
    return sorted_by_morale[:count]

def print_snacks(snacks: list[dict], title: str):
    """Prints a formatted list of snacks."""
    print(f"\n--- {title} ---")
    if not snacks:
        print("No snacks found.")
        return
    for i, snack in enumerate(snacks):
        print(f"{i+1}. {snack['name']}: {snack['calories_per_serving']} calories, {snack['shelf_life_days']} days shelf life, Morale: {snack['morale_boost']}/5")

def main():
    parser = argparse.ArgumentParser(
        description="Apocalypse Snack Sorter: Optimize your survival rations."
    )
    parser.add_argument(
        "--file", 
        type=str, 
        required=True, 
        help="Path to the JSON inventory file (e.g., my_stash.json)"
    )
    parser.add_argument(
        "--sort-by", 
        type=str, 
        choices=['shelf_life', 'calories'], 
        help="Sort snacks by 'shelf_life' or 'calories'"
    )
    parser.add_argument(
        "--morale-boosters", 
        type=int, 
        metavar='COUNT', 
        help="List the top COUNT snacks by morale boost"
    )

    args = parser.parse_args()

    snacks = load_snacks(args.file)

    if args.sort_by == 'shelf_life':
        sorted_snacks = sort_by_shelf_life(snacks)
        print_snacks(sorted_snacks, "Snacks Sorted by Shelf Life (Longest First)")
    elif args.sort_by == 'calories':
        sorted_snacks = sort_by_calories(snacks)
        print_snacks(sorted_snacks, "Snacks Sorted by Caloric Density (Highest First)")
    elif args.morale_boosters is not None:
        if args.morale_boosters < 1:
            print("Error: --morale-boosters count must be at least 1.", file=sys.stderr)
            sys.exit(1)
        top_morale_boosters = find_high_morale_boosters(snacks, args.morale_boosters)
        print_snacks(top_morale_boosters, f"Top {args.morale_boosters} Morale Boosters")
    else:
        print("Error: Please specify an action: --sort-by or --morale-boosters.", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
