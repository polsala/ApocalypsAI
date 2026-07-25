import csv
import sys
import os

# Simple hard‑coded recipe database (recipe name -> required ingredients)
RECIPES = {
    "Bean Soup": {"canned beans", "water", "spice mix"},
    "Rice Pilaf": {"rice", "spice mix", "oil"},
    "Simple Stew": {"canned beans", "rice", "water"},
}

def load_ingredients(path):
    """Read a CSV file (one ingredient per line) and return a set of lower‑cased ingredient names."""
    with open(path, newline='') as f:
        reader = csv.reader(f)
        return {row[0].strip().lower() for row in reader if row}

def suggest_recipes(ingredients):
    """Return a list of recipe names that can be made with the given ingredient set."""
    suggestions = []
    for name, required in RECIPES.items():
        if required.issubset(ingredients):
            suggestions.append(name)
    return suggestions

def main():
    pantry_path = "/data/pantry.csv"
    if not os.path.exists(pantry_path):
        print("Pantry file not found at /data/pantry.csv", file=sys.stderr)
        sys.exit(1)
    ingredients = load_ingredients(pantry_path)
    suggestions = suggest_recipes(ingredients)
    if suggestions:
        print("You can make:")
        for s in suggestions:
            print(f"- {s}")
    else:
        print("No recipes match your pantry. Scavenge more ingredients!")

if __name__ == "__main__":
    main()
