import os
import sys
from src.recipe import load_pantry, suggest

def main() -> None:
    pantry_path = os.getenv("PANTRY_PATH", "/app/pantry.json")
    try:
        pantry = load_pantry(pantry_path)
    except Exception as e:
        print(f"Error loading pantry file: {e}", file=sys.stderr)
        sys.exit(1)

    suggestion = suggest(pantry)
    if suggestion:
        print(f"Suggested recipe: {suggestion['name']}")
        print("Ingredients needed: " + ", ".join(suggestion["ingredients"]))
    else:
        print("No matching recipe found with current pantry items.")

if __name__ == "__main__":
    main()
