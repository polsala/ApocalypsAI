import os
import random
import sys
from pathlib import Path
from typing import List

TEMPLATES = [
    "Radiated Stew with {ing1}, {ing2}, and {ing3}. Enjoy your post‑apocalypse feast!",
    "Mutant Soup featuring {ing1} and a dash of {ing2}.",
    "Wasteland Casserole: {ing1}, {ing2}, {ing3} baked to perfection.",
    "Survivor's Salad with {ing1} tossed with {ing2}.",
    "Scavenger's Skillet: {ing1} meets {ing2} and {ing3}.",
]

def load_ingredients(path: Path) -> List[str]:
    if not path.is_file():
        print(f"[error] Ingredient file not found: {path}", file=sys.stderr)
        sys.exit(1)
    ingredients = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    if not ingredients:
        print("[error] No ingredients found in the file.", file=sys.stderr)
        sys.exit(1)
    return ingredients

def pick_ingredients(ingredients: List[str], count: int) -> List[str]:
    if len(ingredients) <= count:
        return ingredients
    return random.sample(ingredients, count)

def generate_recipe(ingredients: List[str]) -> str:
    # Determine how many ingredients to use (1‑3)
    count = min(3, len(ingredients))
    chosen = pick_ingredients(ingredients, count)
    # Pad missing slots with "..." for template safety
    chosen += ["..."] * (3 - len(chosen))
    template = random.choice(TEMPLATES)
    recipe = template.format(ing1=chosen[0], ing2=chosen[1], ing3=chosen[2])
    return f"🛠️  {recipe}"

def main() -> None:
    # Deterministic mode for tests
    if os.getenv("SCAVENGER_TEST_MODE") == "1":
        random.seed(0)
    else:
        random.seed()
    ingredient_file = Path("/data/ingredients.txt")
    ingredients = load_ingredients(ingredient_file)
    recipe = generate_recipe(ingredients)
    print(recipe)

if __name__ == "__main__":
    main()
