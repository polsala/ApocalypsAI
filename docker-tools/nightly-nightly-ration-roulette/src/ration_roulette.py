import json
import random
import os
import sys

INVENTORY_FILE = os.environ.get("RATIONS_FILE", "rations.json")

def load_inventory(file_path):
    """Loads the rations inventory from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Inventory file '{file_path}' not found. Please create one based on rations_template.json.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{file_path}'. Please check its format.", file=sys.stderr)
        sys.exit(1)

def suggest_meal(inventory_data, meal_type="standard"):
    """
    Suggests a meal based on the specified meal type and available inventory.
    Returns a dictionary of suggested items or None if a meal cannot be composed.
    """
    composition = inventory_data.get("meal_composition", {}).get(meal_type)
    if not composition:
        print(f"Error: Meal type '{meal_type}' not found in meal_composition.", file=sys.stderr)
        return None

    suggested_meal = {}
    for category in composition:
        available_items = [item for item in inventory_data.get("inventory", {}).get(category, []) if item.get("quantity", 0) > 0]
        if not available_items:
            print(f"Warning: No items available for category '{category}' for '{meal_type}' meal. Skipping.", file=sys.stderr)
            continue
        
        chosen_item = random.choice(available_items)
        suggested_meal[category] = chosen_item["name"]
    
    return suggested_meal

def main():
    meal_type = sys.argv[1] if len(sys.argv) > 1 else "standard"
    
    inventory_data = load_inventory(INVENTORY_FILE)
    if not inventory_data:
        sys.exit(1) # Error already printed by load_inventory

    print(f"--- ApocalypsAI Ration Roulette: {meal_type.capitalize()} Meal ---")
    meal = suggest_meal(inventory_data, meal_type)

    if meal:
        if not meal: # If meal is an empty dict, no items were suggested
            print("Could not compose a meal with available rations.")
        else:
            for category, item_name in meal.items():
                print(f"- {category.capitalize()}: {item_name}")
            print("\nEnjoy your varied sustenance!")
    else:
        print("Failed to suggest a meal. Check your inventory and meal compositions.")

if __name__ == "__main__":
    main()
