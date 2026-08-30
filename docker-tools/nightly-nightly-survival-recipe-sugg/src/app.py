import json
import os
from src.recipes import RECIPES


def load_pantry(path):
    """Load pantry JSON file; return list of lower‑cased ingredient strings."""
    try:
        with open(path, "r") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Pantry file must contain a JSON list of ingredient strings.")
            return [str(item).lower() for item in data]
    except FileNotFoundError:
        return []


def suggest_recipes(pantry):
    """Return a list of recipe names whose ingredients are all present in *pantry*.

    *pantry* should be an iterable of lower‑cased ingredient strings.
    """
    pantry_set = set(pantry)
    suggestions = []
    for name, ingredients in RECIPES.items():
        if set(ingredients).issubset(pantry_set):
            suggestions.append(name)
    return suggestions


def main():
    pantry_path = os.getenv("PANTRY_PATH", "/app/pantry.json")
    pantry = load_pantry(pantry_path)
    suggestions = suggest_recipes(pantry)
    if suggestions:
        print("You can make:")
        for r in suggestions:
            print(f"- {r}")
    else:
        print("No recipes match your pantry.")


if __name__ == "__main__":
    main()
