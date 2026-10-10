import json
import random
from typing import List, Dict, Optional

def load_pantry(path: str) -> List[str]:
    """Load a JSON file containing a list of ingredient strings."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Pantry JSON must be a list of ingredient strings")
    return data

def load_recipes() -> List[Dict[str, List[str]]]:
    """Return a hard‑coded list of recipes.
    Each recipe is a dict with keys 'name' and 'ingredients'.
    """
    return [
        {"name": "Pancakes", "ingredients": ["flour", "egg", "milk", "sugar", "butter"]},
        {"name": "Omelette", "ingredients": ["egg", "milk", "butter"]},
        {"name": "French Toast", "ingredients": ["egg", "milk", "bread", "sugar"]},
        {"name": "Butter Toast", "ingredients": ["bread", "butter"]},
    ]

def find_matching(pantry: List[str], recipes: List[Dict[str, List[str]]]) -> List[Dict[str, List[str]]]:
    """Return recipes whose ingredient sets are subsets of the pantry."""
    pantry_set = set(pantry)
    return [r for r in recipes if set(r["ingredients"]).issubset(pantry_set)]

def suggest(pantry: List[str]) -> Optional[Dict[str, List[str]]]:
    """Pick a random matching recipe, or return None if none match."""
    recipes = load_recipes()
    matches = find_matching(pantry, recipes)
    if not matches:
        return None
    return random.choice(matches)
