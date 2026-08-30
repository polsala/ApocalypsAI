import csv
import sys
import pathlib

def load_inventory(path):
    """Read a CSV file where each line is an ingredient name and return a set of lower‑cased items."""
    items = set()
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                items.add(row[0].strip().lower())
    return items

# Simple built‑in recipe database
RECIPES = [
    {"name": "Bean Soup", "ingredients": {"beans", "water", "salt"}},
    {"name": "Rice Pilaf", "ingredients": {"rice", "water", "oil"}},
    {"name": "Peanut Butter Toast", "ingredients": {"bread", "peanut butter"}},
    {"name": "Fruit Salad", "ingredients": {"apple", "banana", "orange"}},
]

def suggest_recipes(inventory):
    """Return a list of recipe names whose ingredient sets are all present in *inventory*."""
    suggestions = []
    for r in RECIPES:
        if r["ingredients"].issubset(inventory):
            suggestions.append(r["name"])
    return suggestions

def main():
    inventory_path = pathlib.Path("/data/inventory.csv")
    if not inventory_path.is_file():
        print("Inventory file not found at /data/inventory.csv", file=sys.stderr)
        sys.exit(1)
    inventory = load_inventory(inventory_path)
    suggestions = suggest_recipes(inventory)
    if suggestions:
        print("You can make:")
        for s in suggestions:
            print("- " + s)
    else:
        print("No recipes match your pantry items.")

if __name__ == "__main__":
    main()
