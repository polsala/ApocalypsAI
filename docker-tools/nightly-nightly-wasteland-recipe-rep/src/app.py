import json
import argparse
import sys

def load_recipes(filepath="src/recipes.json"):
    """Loads recipes from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(json.dumps({"error": f"Recipe file not found at {filepath}"}), file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(json.dumps({"error": f"Invalid JSON in recipe file at {filepath}"}), file=sys.stderr)
        sys.exit(1)

def find_matching_recipes(available_ingredients_str, all_recipes):
    """Finds recipes that can be made with the available ingredients."""
    if not available_ingredients_str:
        return []

    available_ingredients = {ing.strip().lower() for ing in available_ingredients_str.split(',')}
    matching_recipes = []

    for recipe in all_recipes:
        recipe_ingredients = {ing.strip().lower() for ing in recipe.get('ingredients', [])}
        if recipe_ingredients and recipe_ingredients.issubset(available_ingredients):
            matching_recipes.append(recipe)
            
    return matching_recipes

def main():
    parser = argparse.ArgumentParser(description="Wasteland Recipe Replicator: Find recipes based on available ingredients.")
    parser.add_argument('--ingredients', type=str, default="",
                        help="Comma-separated list of available ingredients (e.g., 'mutant fungus,stale bread').")

    args = parser.parse_args()

    all_recipes = load_recipes()
    if all_recipes is None: # Error already printed by load_recipes
        sys.exit(1)

    found_recipes = find_matching_recipes(args.ingredients, all_recipes)
    print(json.dumps(found_recipes, indent=2))

if __name__ == "__main__":
    main()
