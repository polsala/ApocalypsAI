import csv
import sys
from typing import Dict, List, Set

# ---------------------------------------------------------------------------
# Mock rationale: Hard‑coded recipe database keeps the utility self‑contained
# and deterministic for offline testing.
# ---------------------------------------------------------------------------

RECIPE_DB: Dict[str, Set[str]] = {
    "Mystic Muesli": {"oats", "honey", "nuts"},
    "Radiation‑Free Ramen": {"noodles", "broth", "egg"},
    "Scavenger's Stew": {"carrot", "potato", "beans"},
    "Wasteland Wrap": {"tortilla", "cheese", "tomato"},
}


def load_inventory(csv_path: str) -> Dict[str, int]:
    """Parse a CSV inventory file.

    The CSV must have a header row with `ingredient,quantity`.
    Returns a mapping of ingredient (lower‑cased) to integer quantity.
    """
    inventory: Dict[str, int] = {}
    try:
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ingredient = row["ingredient"].strip().lower()
                try:
                    qty = int(row["quantity"].strip())
                except ValueError:
                    qty = 0
                if qty > 0:
                    inventory[ingredient] = inventory.get(ingredient, 0) + qty
    except FileNotFoundError:
        print(f"Error: file '{csv_path}' not found.", file=sys.stderr)
        sys.exit(1)
    return inventory


def suggest_recipes(inventory: Dict[str, int]) -> List[str]:
    """Return a list of recipe names that can be made with the given inventory.

    A recipe is possible if **all** its required ingredients are present
    with a quantity of at least 1.
    """
    possible: List[str] = []
    available = set(inventory.keys())
    for recipe, ingredients in RECIPE_DB.items():
        if ingredients.issubset(available):
            possible.append(recipe)
    return possible


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python app.py <inventory.csv>")
        sys.exit(1)
    csv_path = sys.argv[1]
    inventory = load_inventory(csv_path)
    recipes = suggest_recipes(inventory)
    if recipes:
        print("Possible recipes based on your pantry:")
        for r in recipes:
            print(f"- {r}")
    else:
        print("No recipes can be made with the current inventory.")


if __name__ == "__main__":
    main()
