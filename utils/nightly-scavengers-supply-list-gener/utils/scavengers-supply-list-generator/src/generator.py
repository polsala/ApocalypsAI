import json
import os
import sys

class ScavengerSupplyGenerator:
    def __init__(self, data_path=None):
        self.data_path = data_path if data_path else os.path.join(os.path.dirname(__file__), 'data.json')
        self.supplies = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.data_path):
            print(f"Error: Data file not found at {self.data_path}", file=sys.stderr)
            return {}
        try:
            with open(self.data_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.data_path}. Check file integrity.", file=sys.stderr)
            return {}

    def get_supply_list(self, item_name: str):
        item_name_lower = item_name.lower()
        item_info = self.supplies.get(item_name_lower)

        if not item_info:
            return {
                "item": item_name,
                "found": False,
                "message": f"No information found for '{item_name}'. Try a different item or use --list to see available items."
            }

        return {
            "item": item_name,
            "found": True,
            "description": item_info.get("description", "No description available."),
            "components": item_info.get("components", []),
            "locations": item_info.get("locations", []),
            "alternatives": item_info.get("alternatives", [])
        }

    def list_available_items(self):
        return sorted(list(self.supplies.keys()))

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate scavenging supply lists for post-apocalyptic survival.")
    parser.add_argument("item", nargs='?', help="The item to generate a supply list for (e.g., 'flashlight').")
    parser.add_argument("--list", action="store_true", help="List all available items.")

    args = parser.parse_args()

    generator = ScavengerSupplyGenerator()

    if args.list:
        items = generator.list_available_items()
        if items:
            print("Available items for scavenging:")
            for item in items:
                print(f"- {item.capitalize()}")
        else:
            print("No items available in the supply database.")
        return

    if not args.item:
        parser.print_help()
        sys.exit(1)

    result = generator.get_supply_list(args.item)

    if result["found"]:
        print(f"\n--- Scavenging Report for: {result['item'].capitalize()} ---")
        print(f"Description: {result['description']}")

        if result["components"]:
            print("\nPotential Components:")
            for comp in result["components"]:
                print(f"- {comp['name'].capitalize()} ({comp['quantity']})")
        else:
            print("\nNo specific components listed.")

        if result["locations"]:
            print("\nLikely Scavenging Locations:")
            for loc in result["locations"]:
                print(f"- {loc.capitalize()}")
        else:
            print("\nNo specific locations suggested.")

        if result["alternatives"]:
            print("\nPossible Alternatives:")
            for alt in result["alternatives"]:
                print(f"- {alt.capitalize()}")
        else:
            print("\nNo direct alternatives suggested.")
    else:
        print(f"\n{result['message']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
