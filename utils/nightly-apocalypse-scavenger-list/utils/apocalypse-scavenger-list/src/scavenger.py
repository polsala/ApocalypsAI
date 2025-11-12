import json
import argparse
import os

class ScavengerListGenerator:
    def __init__(self, items_filepath='src/items.json'):
        self.items_filepath = os.path.join(os.path.dirname(__file__), items_filepath)
        self.items = self._load_items()

    def _load_items(self):
        try:
            with open(self.items_filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Items file not found at {self.items_filepath}")
            return []
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.items_filepath}")
            return []

    def generate_list(self, categories, count=None):
        if not self.items:
            return []

        filtered_items = []
        for item in self.items:
            if 'all' in categories or item.get('category') in categories:
                filtered_items.append(item)
        
        # Sort by priority (descending), then by name (ascending) for stable order
        sorted_items = sorted(filtered_items, key=lambda x: (-x.get('priority', 0), x.get('name', '')))

        if count is not None:
            return sorted_items[:count]
        return sorted_items

    def print_list(self, items, categories):
        if not items:
            print(f"No items found for categories: {', '.join(categories)}")
            return

        print(f"\n--- Apocalypse Scavenging List (Categories: {', '.join(categories)}) ---")
        for i, item in enumerate(items):
            print(f"{i+1}. {item['name']} ({item['category'].capitalize()}, Priority: {item['priority']})")
        print("-------------------------------------------------------------------\n")

def main():
    parser = argparse.ArgumentParser(description="Generate a prioritized scavenging list for the post-apocalypse.")
    parser.add_argument('--categories', nargs='+', default=['all'],
                        help="Space-separated list of categories (e.g., survival food tools). Use 'all' for all categories.")
    parser.add_argument('--count', type=int, help="Maximum number of items to display.")

    args = parser.parse_args()

    generator = ScavengerListGenerator()
    scavenge_list = generator.generate_list(args.categories, args.count)
    generator.print_list(scavenge_list, args.categories)

if __name__ == '__main__':
    main()
