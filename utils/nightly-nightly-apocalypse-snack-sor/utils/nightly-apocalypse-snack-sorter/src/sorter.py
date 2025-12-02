import sys
import os

def categorize_item(item_name: str) -> dict:
    """Categorizes a single food item based on keywords."""
    item_name_lower = item_name.lower()

    # Shelf Stability Categories
    shelf_stability = "Unknown Stability" # Default if no specific keywords match
    if any(keyword in item_name_lower for keyword in ["canned", "dried", "rice", "pasta", "honey", "salt", "jerky", "sugar", "flour", "beans", "lentils", "oats"]):
        shelf_stability = "Long-Haul"
    elif any(keyword in item_name_lower for keyword in ["potatoes", "apples", "cheese", "crackers", "nuts", "chocolate", "coffee", "chips", "soda", "bottled water", "tea", "jam", "syrup"]):
        shelf_stability = "Mid-Term"
    elif any(keyword in item_name_lower for keyword in ["milk", "bread", "fresh", "fruit", "vegetables", "meat", "yogurt", "eggs", "fish", "dairy"]):
        shelf_stability = "Perishable Panic"

    # Comfort Level Categories
    comfort_level = "Pure Sustenance" # Default if no specific keywords match
    if any(keyword in item_name_lower for keyword in ["chocolate", "coffee", "tea", "cookies", "ice cream", "cake", "pie", "candy bar", "hot cocoa"]):
        comfort_level = "Soul Soother"
    elif any(keyword in item_name_lower for keyword in ["chips", "soda", "candy", "gum", "donuts", "popcorn", "pretzels"]):
        comfort_level = "Morale Booster"

    return {
        "item": item_name,
        "shelf_stability": shelf_stability,
        "comfort_level": comfort_level
    }

def read_items_from_file(filepath: str) -> list[str]:
    """Reads food items from a specified file, one per line."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        items = [line.strip() for line in f if line.strip()]
    return items

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 sorter.py <input_file_path>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        items = read_items_from_file(input_file)
        print("Apocalypse Snack Sorter Report:\n")
        for item in items:
            category_info = categorize_item(item)
            print(f"--- {category_info['item']} ---")
            print(f"  Shelf Stability: {category_info['shelf_stability']}")
            print(f"  Comfort Level: {category_info['comfort_level']}\n")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
