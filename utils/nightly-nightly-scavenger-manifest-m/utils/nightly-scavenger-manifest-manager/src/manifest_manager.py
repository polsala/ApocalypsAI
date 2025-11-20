import json
import os
from datetime import datetime

class ManifestManager:
    def __init__(self, manifest_file="manifest.json"):
        self.manifest_file = manifest_file
        self.items = []
        self._load_manifest()
        self._next_id = max([item['id'] for item in self.items]) + 1 if self.items else 1

    def _load_manifest(self):
        if os.path.exists(self.manifest_file):
            try:
                with open(self.manifest_file, 'r') as f:
                    self.items = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Manifest file '{self.manifest_file}' is corrupted. Starting with an empty manifest.")
                self.items = []
        else:
            self.items = []

    def save_manifest(self):
        with open(self.manifest_file, 'w') as f:
            json.dump(self.items, f, indent=4)

    def add_item(self, name, description, quantity, tags):
        item = {
            "id": self._next_id,
            "name": name,
            "description": description,
            "quantity": quantity,
            "tags": [tag.strip().lower() for tag in tags.split(',')] if tags else [],
            "added_date": datetime.now().isoformat()
        }
        self.items.append(item)
        self._next_id += 1
        return item

    def list_items(self):
        if not self.items:
            return []
        return sorted(self.items, key=lambda x: x['id'])

    def search_items(self, query):
        query_lower = query.lower()
        results = []
        for item in self.items:
            if query_lower in item['name'].lower() or \
               query_lower in item['description'].lower() or \
               any(query_lower in tag for tag in item['tags']):
                results.append(item)
        return results

    def remove_item(self, item_id):
        initial_len = len(self.items)
        self.items = [item for item in self.items if item['id'] != item_id]
        return len(self.items) < initial_len

def main():
    manager = ManifestManager()
    print("Welcome to the Scavenger's Manifest Manager!")
    print("Type 'help' for commands, 'exit' to save and quit.")

    while True:
        try:
            command = input("> ").strip().lower()
            if command == "exit":
                manager.save_manifest()
                print("Manifest saved. Goodbye, survivor!")
                break
            elif command == "help":
                print("\nAvailable commands:")
                print("  add - Add a new item to the manifest.")
                print("  list - Display all items in the manifest.")
                print("  search <query> - Search items by name, description, or tags.")
                print("  remove <item_id> - Remove an item by its ID.")
                print("  save - Manually save the manifest.")
                print("  load - Manually load the manifest from file (overwrites current in-memory state).")
                print("  exit - Save and exit the program.")
            elif command == "add":
                name = input("  Item Name: ")
                description = input("  Description: ")
                quantity = int(input("  Quantity: "))
                tags = input("  Tags (comma-separated, e.g., food,medical): ")
                manager.add_item(name, description, quantity, tags)
                print(f"  '{name}' added to manifest.")
            elif command == "list":
                items = manager.list_items()
                if not items:
                    print("  Manifest is empty.")
                else:
                    print("\n--- Current Manifest ---")
                    for item in items:
                        print(f"  ID: {item['id']}")
                        print(f"    Name: {item['name']}")
                        print(f"    Desc: {item['description']}")
                        print(f"    Qty: {item['quantity']}")
                        print(f"    Tags: {', '.join(item['tags'])}")
                        print(f"    Added: {item['added_date']}")
                        print("  ------------------------")
            elif command.startswith("search "):
                query = command[len("search "):].strip()
                results = manager.search_items(query)
                if not results:
                    print(f"  No items found matching '{query}'.")
                else:
                    print(f"\n--- Search Results for '{query}' ---")
                    for item in results:
                        print(f"  ID: {item['id']}")
                        print(f"    Name: {item['name']}")
                        print(f"    Desc: {item['description']}")
                        print(f"    Qty: {item['quantity']}")
                        print(f"    Tags: {', '.join(item['tags'])}")
                        print(f"    Added: {item['added_date']}")
                        print("  ------------------------")
            elif command.startswith("remove "):
                try:
                    item_id = int(command[len("remove "):].strip())
                    if manager.remove_item(item_id):
                        print(f"  Item ID {item_id} removed.")
                    else:
                        print(f"  Item ID {item_id} not found.")
                except ValueError:
                    print("  Invalid item ID. Please provide a number.")
            elif command == "save":
                manager.save_manifest()
                print("  Manifest manually saved.")
            elif command == "load":
                manager._load_manifest() # Directly call internal load to refresh
                print("  Manifest manually loaded from file.")
            else:
                print("  Unknown command. Type 'help' for a list of commands.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
