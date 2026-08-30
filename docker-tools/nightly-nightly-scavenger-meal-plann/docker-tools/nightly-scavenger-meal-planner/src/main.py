import sys
import random
from pathlib import Path

# Fixed seed for deterministic output
random.seed(42)

RECIPES = [
    {
        "name": "Spaghetti with Tomato Sauce and Canned Beans",
        "ingredients": {"spaghetti", "tomato sauce", "canned beans"},
    },
    {
        "name": "Bean Soup",
        "ingredients": {"canned beans", "water", "salt"},
    },
    {
        "name": "Rice Porridge",
        "ingredients": {"rice", "water"},
    },
    {
        "name": "Mystery Stew",
        "ingredients": {"canned meat", "canned beans", "water"},
    },
]

def load_ingredients(path: Path) -> set[str]:
    """Read ingredients file, one per line, case‑insensitive."""
    if not path.is_file():
        print(f"Ingredient file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return {line.strip().lower() for line in path.read_text().splitlines() if line.strip()}

def find_matching_recipes(pantry: set[str]) -> list[dict]:
    matches = []
    for recipe in RECIPES:
        if recipe["ingredients"].issubset(pantry):
            matches.append(recipe)
    return matches

def suggest_recipe(pantry: set[str]) -> str:
    matches = find_matching_recipes(pantry)
    if not matches:
        return "No viable recipe found with given ingredients."
    return random.choice(matches)["name"]

def main():
    ingredients_path = Path("/app/ingredients.txt")
    pantry = load_ingredients(ingredients_path)
    suggestion = suggest_recipe(pantry)
    print(f"Recipe: {suggestion}")

if __name__ == "__main__":
    main()
