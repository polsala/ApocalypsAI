import argparse
from typing import List, Dict, Any

class Recipe:
    """Represents a single rad-resistant recipe."""
    def __init__(self, name: str, ingredients: List[str], instructions: List[str], tip: str):
        self.name = name
        self.ingredients = [ing.lower() for ing in ingredients] # Normalize ingredients
        self.instructions = instructions
        self.tip = tip

    def __repr__(self) -> str:
        return f"Recipe(name='{self.name}', ingredients={self.ingredients})"

    def get_details(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "tip": self.tip
        }

class SurvivalCookbook:
    """Manages a collection of rad-resistant recipes."""
    def __init__(self):
        self._recipes: List[Recipe] = []
        self._load_default_recipes() # Load some initial survival recipes

    def _load_default_recipes(self):
        """Populates the cookbook with essential post-apocalyptic recipes."""
        self.add_recipe(Recipe(
            name="Bunker Bean Stew",
            ingredients=["canned beans", "water", "salt", "scavenged greens"],
            instructions=[
                "Combine canned beans, water, and a pinch of salt in a pot.",
                "Heat over a low flame until simmering.",
                "If you're lucky enough to find any scavenged greens, chop them and add for extra nutrients.",
                "Serve hot with stale bread for dipping."
            ],
            tip="A true survivor knows how to make a feast from a few beans and a prayer."
        ))
        self.add_recipe(Recipe(
            name="Stale Bread & Water Gruel",
            ingredients=["stale bread", "water"],
            instructions=[
                "Break stale bread into small pieces.",
                "Soak in water until soft.",
                "Consume slowly."
            ],
            tip="Hydration is key, even if your meal is mostly liquid bread."
        ))
        self.add_recipe(Recipe(
            name="Mystery Meat Skewers",
            ingredients=["mystery meat", "firewood", "sharp stick"],
            instructions=[
                "Carefully skewer chunks of mystery meat onto a sharp stick.",
                "Build a small, controlled fire using scavenged firewood.",
                "Roast the meat over the flames until thoroughly cooked (or until you can't wait any longer).",
                "Eat quickly before the rad-roaches get to it."
            ],
            tip="Always cook mystery meat thoroughly. Better safe than glowing."
        ))
        self.add_recipe(Recipe(
            name="Foraged Berry Mash",
            ingredients=["foraged berries", "clean water"],
            instructions=[
                "Carefully inspect foraged berries for any signs of mutation or toxicity.",
                "Wash thoroughly with clean water.",
                "Mash berries into a pulp.",
                "Enjoy a rare taste of sweetness. (Consume at your own risk!)"
            ],
            tip="Not all berries are edible. When in doubt, consult your local wasteland botanist (or just don't eat it)."
        ))
        self.add_recipe(Recipe(
            name="Dusty Potato Pancakes",
            ingredients=["potatoes", "flour", "water", "cooking oil"],
            instructions=[
                "Peel and grate potatoes (if you have a grater, otherwise mash them).",
                "Mix with a small amount of flour and water to form a batter.",
                "Heat cooking oil in a pan (if you have one).",
                "Fry small portions of the batter until golden brown.",
                "A surprisingly comforting meal in the desolate landscape."
            ],
            tip="Potatoes are a versatile survival crop. Learn to love them."
        ))


    def add_recipe(self, recipe: Recipe):
        """Adds a new recipe to the cookbook."""
        self._recipes.append(recipe)

    def get_all_recipes(self) -> List[Recipe]:
        """Returns all recipes in the cookbook."""
        return list(self._recipes)

def recommend_recipes(available_ingredients: List[str], cookbook: SurvivalCookbook) -> List[Dict[str, Any]]:
    """
    Recommends recipes based on available ingredients.
    Returns a list of dictionaries, each containing recipe details and match count,
    sorted by the number of matching ingredients (descending).
    """
    available_ingredients_lower = {ing.lower() for ing in available_ingredients}
    matched_recipes = []

    for recipe in cookbook.get_all_recipes():
        match_count = 0
        for required_ingredient in recipe.ingredients:
            if required_ingredient in available_ingredients_lower:
                match_count += 1
        
        # Only recommend recipes if at least one ingredient matches
        if match_count > 0:
            recipe_details = recipe.get_details()
            recipe_details["match_count"] = match_count
            recipe_details["total_ingredients"] = len(recipe.ingredients)
            matched_recipes.append(recipe_details)

    # Sort by match count in descending order
    matched_recipes.sort(key=lambda x: x["match_count"], reverse=True)
    return matched_recipes

def main():
    parser = argparse.ArgumentParser(
        description="Recommend rad-resistant recipes based on available ingredients."
    )
    parser.add_argument(
        "--ingredients",
        nargs=":", # Use ':' to allow 0 or more arguments, but still require it for clarity
        default=[],
        help="A space-separated list of ingredients you have on hand (e.g., 'canned beans' 'water')."
    )

    args = parser.parse_args()

    # If no ingredients are provided after --ingredients, nargs=':' will result in an empty list.
    # We should handle the case where --ingredients is present but empty, or not present.
    # argparse.ArgumentParser.parse_args() will return an empty list for nargs=':' if no values follow.
    # If --ingredients is not provided at all, args.ingredients will be the default [].
    # Let's ensure it's treated as required for the logic to make sense.
    if not args.ingredients:
        print("Error: Please provide at least one ingredient using --ingredients.")
        sys.exit(1)

    cookbook = SurvivalCookbook()
    recommendations = recommend_recipes(args.ingredients, cookbook)

    print("\n--- Rad-Resistant Recipe Recommendations ---\n")

    if not recommendations:
        print("No recipes found matching your ingredients. Time to get creative (or hungry).")
        return

    for i, recipe_data in enumerate(recommendations):
        print(f"{i+1}. **{recipe_data['name']} (Matches {recipe_data['match_count']}/{recipe_data['total_ingredients']} ingredients)**")
        print(f"   Ingredients: {', '.join(recipe_data['ingredients'])}")
        print("   Instructions:")
        for step in recipe_data['instructions']:
            print(f"   * {step}")
        print(f"   *Survival Tip: {recipe_data['tip']}*\n")

if __name__ == "__main__":
    import sys
    main()
