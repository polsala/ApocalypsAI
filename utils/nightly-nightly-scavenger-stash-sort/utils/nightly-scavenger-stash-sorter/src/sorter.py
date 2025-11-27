import argparse
import sys
from typing import List, Dict, Any

class StashSorter:
    """
    Categorizes scavenged items based on predefined rules.
    """

    CATEGORIZATION_RULES: Dict[str, Dict[str, Any]] = {
        "Food": {
            "keywords": ["apple", "can", "ration", "berry", "water", "jerky", "beans", "mushroom"],
            "priority": "High",
            "location": "Pantry"
        },
        "Tools": {
            "keywords": ["wrench", "hammer", "screwdriver", "saw", "knife", "axe", "pliers"],
            "priority": "Medium",
            "location": "Workshop"
        },
        "Materials": {
            "keywords": ["scrap metal", "wood plank", "wire", "cloth", "plastic", "copper", "steel"],
            "priority": "Medium",
            "location": "Storage Shed"
        },
        "Medical": {
            "keywords": ["bandages", "antiseptic", "painkillers", "medkit", "antibiotics", "gauze"],
            "priority": "High",
            "location": "Infirmary"
        },
        "Junk": {
            "keywords": ["broken toy", "rusty nail", "old boot", "pebble", "debris", "rubble"],
            "priority": "Low",
            "location": "Disposal Pile"
        }
    }

    def categorize_item(self, item_name: str) -> Dict[str, str]:
        """
        Categorizes a single item based on its name and predefined rules.
        """
        item_lower = item_name.lower()
        for category, rules in self.CATEGORIZATION_RULES.items():
            for keyword in rules["keywords"]:
                if keyword in item_lower:
                    return {
                        "category": category,
                        "priority": rules["priority"],
                        "location": rules["location"]
                    }
        return {
            "category": "Uncategorized",
            "priority": "Unknown",
            "location": "Undetermined"
        }

    def sort_stash(self, item_list: List[str]) -> List[Dict[str, str]]:
        """
        Processes a list of items and returns their categorized details.
        """
        sorted_items = []
        for item in item_list:
            category_info = self.categorize_item(item.strip())
            sorted_items.append({
                "item": item.strip(),
                **category_info
            })
        return sorted_items

    def display_report(self, sorted_items: List[Dict[str, str]]) -> None:
        """
        Prints a formatted report of the sorted items.
        """
        print("--- Scavenger's Stash Report ---")
        if not sorted_items:
            print("\nNo items to report. Time to go scavenging!\n")
            return

        for item_data in sorted_items:
            print(f"\nItem: {item_data['item']}")
            print(f"  Category: {item_data['category']}")
            print(f"  Priority: {item_data['priority']}")
            print(f"  Location: {item_data['location']}")
        print("\n--- End of Report ---")

def main():
    parser = argparse.ArgumentParser(
        description="Categorize your scavenged items for optimal post-apocalyptic organization."
    )
    parser.add_argument(
        "--items",
        type=str,
        help="Comma-separated list of items (e.g., 'apple,wrench,scrap metal')"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to a file containing items, one per line."
    )

    args = parser.parse_args()
    sorter = StashSorter()
    items_to_sort: List[str] = []

    if args.items:
        items_to_sort = [item.strip() for item in args.items.split(',') if item.strip()]
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                items_to_sort = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file '{args.file}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    sorted_stash = sorter.sort_stash(items_to_sort)
    sorter.display_report(sorted_stash)

if __name__ == "__main__":
    main()
