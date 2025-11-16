import sys
from typing import List, Dict, Tuple

# Define categorization rules
# Each category has a list of keywords. If an item contains any of these keywords (case-insensitive),
# it's assigned to that category. Order matters for overlapping keywords (e.g., "canned" might be in multiple).
# More specific rules should come before more general ones if there's a potential for overlap.
CATEGORIES: Dict[str, List[str]] = {
    "Long-Term Survival": [
        "canned", "dried", "rice", "pasta", "beans", "lentils", "oats", "flour",
        "sugar", "salt", "honey", "jerky", "mre", "powdered milk", "hard tack",
        "water purification", "vitamins", "nuts", "seeds", "oil", "syrup"
    ],
    "Short-Term Morale Boost": [
        "chocolate", "coffee", "tea", "candy", "soda", "alcohol", "spices",
        "cookies", "chips", "gum", "jam", "jelly", "condiments", "sweet", "treat"
    ],
    "Immediate Consumption": [
        "fresh", "milk", "eggs", "meat", "fish", "fruit", "vegetables", "bread",
        "yogurt", "cheese", "dairy", "berries", "greens", "produce"
    ]
}

def categorize_item(item: str) -> str:
    """
    Categorizes a single food item based on predefined keywords.
    """
    item_lower = item.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in item_lower:
                return category
    return "Uncategorized" # Fallback for items that don't match any category

def sort_inventory(items: List[str]) -> Dict[str, List[str]]:
    """
    Sorts a list of food items into predefined categories.
    """
    sorted_items: Dict[str, List[str]] = {
        "Long-Term Survival": [],
        "Short-Term Morale Boost": [],
        "Immediate Consumption": [],
        "Uncategorized": [] # To catch items not matching any rule
    }

    for item in items:
        category = categorize_item(item)
        sorted_items[category].append(item)

    # Ensure all defined categories are present, even if empty
    for category_name in CATEGORIES.keys():
        if category_name not in sorted_items:
            sorted_items[category_name] = []

    return sorted_items

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/sorter.py \"Item 1\" \"Item 2\" ...")
        sys.exit(1)

    items_to_sort = sys.argv[1:]
    sorted_inventory = sort_inventory(items_to_sort)

    print("--- Apocalypse Snack Inventory ---")
    # Print defined categories first, then Uncategorized
    for category_name in CATEGORIES.keys():
        if sorted_inventory[category_name]:
            print(f"{category_name}:")
            for item in sorted_inventory[category_name]:
                print(f"  - {item}")
    
    # Also print Uncategorized items if any
    if "Uncategorized" in sorted_inventory and sorted_inventory["Uncategorized"]:
        print("Uncategorized:")
        for item in sorted_inventory["Uncategorized"]: 
            print(f"  - {item}")


if __name__ == "__main__":
    main()
