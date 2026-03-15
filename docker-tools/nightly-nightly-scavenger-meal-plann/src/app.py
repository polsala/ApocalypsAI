import sys
import random
import pathlib

def load_ingredients(path):
    try:
        with open(path) as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Ingredient file not found: {path}", file=sys.stderr)
        sys.exit(1)

RECIPES = [
    {
        "name": "Radiated Rat Stew",
        "ingredients": {"rat", "water", "spice"},
        "instructions": "Boil rat in water, add spice, simmer until glowing."
    },
    {
        "name": "Mushroom Mutant Soup",
        "ingredients": {"mushroom", "water", "salt"},
        "instructions": "Blend mushrooms with water and a pinch of salt."
    },
    {
        "name": "Canned Cactus Salad",
        "ingredients": {"cactus", "oil", "vinegar"},
        "instructions": "Slice cactus, drizzle oil and vinegar."
    },
]

def find_recipe(available):
    matches = []
    for r in RECIPES:
        if r["ingredients"].issubset(available):
            matches.append(r)
    return matches

def main():
    path = "ingredients.txt"
    ingredients = set(load_ingredients(path))
    matches = find_recipe(ingredients)
    random.seed(42)  # deterministic selection for testing
    if matches:
        recipe = random.choice(matches)
        print(f"Recipe: {recipe['name']}")
        print(f"Ingredients needed: {', '.join(sorted(recipe['ingredients']))}")
        print(f"Instructions: {recipe['instructions']}")
    else:
        print("No matching recipe found with given ingredients.")

if __name__ == "__main__":
    main()
