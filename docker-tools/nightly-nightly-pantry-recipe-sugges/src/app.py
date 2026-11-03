import sys
import pathlib

def load_ingredients(path):
    with open(path) as f:
        return {line.strip().lower() for line in f if line.strip()}

RECIPES = {
    "Grilled Cheese": {"bread", "cheese", "butter"},
    "Tomato Soup": {"tomato", "water", "salt"},
    "Peanut Butter Sandwich": {"bread", "peanut butter"},
    "Cheese Pizza": {"bread", "cheese", "tomato"},
}

def get_possible_recipes(available):
    possible = []
    for name, ingredients in RECIPES.items():
        if ingredients.issubset(available):
            possible.append(name)
    return possible

def main():
    ingredients_file = pathlib.Path("ingredients.txt")
    if not ingredients_file.is_file():
        print("ingredients.txt not found in /app")
        sys.exit(1)
    available = load_ingredients(ingredients_file)
    recipes = get_possible_recipes(available)
    if recipes:
        print("You can make:")
        for r in recipes:
            print(f"- {r}")
    else:
        print("No recipes match your ingredients.")

if __name__ == "__main__":
    main()
