import json
import os
from typing import List, Dict, Any

class Snack:
    def __init__(self, name: str, shelf_life_days: int, calories_per_serving: int, comfort_factor: int):
        if not (1 <= comfort_factor <= 5):
            raise ValueError("Comfort factor must be between 1 and 5.")
        self.name = name
        self.shelf_life_days = shelf_life_days
        self.calories_per_serving = calories_per_serving
        self.comfort_factor = comfort_factor

    def __repr__(self) -> str:
        return (f"Snack(name='{self.name}', shelf_life_days={self.shelf_life_days}, "
                f"calories_per_serving={self.calories_per_serving}, comfort_factor={self.comfort_factor})")

    def __lt__(self, other: 'Snack') -> bool:
        # Primary sort: shortest shelf-life first (ascending)
        if self.shelf_life_days != other.shelf_life_days:
            return self.shelf_life_days < other.shelf_life_days
        # Secondary sort: highest calories per serving (descending)
        if self.calories_per_serving != other.calories_per_serving:
            return self.calories_per_serving > other.calories_per_serving
        # Tertiary sort: highest comfort factor (descending)
        return self.comfort_factor > other.comfort_factor

def load_snacks(file_path: str) -> List[Snack]:
    """Loads snack data from a JSON file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Snack data file not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    snacks = []
    for item in data:
        try:
            snacks.append(Snack(
                name=item['name'],
                shelf_life_days=item['shelf_life_days'],
                calories_per_serving=item['calories_per_serving'],
                comfort_factor=item['comfort_factor']
            ))
        except KeyError as e:
            raise ValueError(f"Missing key in snack data: {e} in item {item}")
        except ValueError as e:
            raise ValueError(f"Invalid value in snack data: {e} in item {item}")
    return snacks

def sort_snacks(snacks: List[Snack]) -> List[Snack]:
    """Sorts snacks based on defined priority rules."""
    return sorted(snacks)

def main():
    script_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(script_dir, '..', 'data', 'snacks.json')

    try:
        snacks = load_snacks(data_file_path)
        if not snacks:
            print("No snacks found in data file. Add some to data/snacks.json!")
            return

        sorted_snacks = sort_snacks(snacks)

        print("\n--- Prioritized Snack Consumption Plan ---")
        for i, snack in enumerate(sorted_snacks):
            print(f"{i+1}. {snack.name} (Shelf Life: {snack.shelf_life_days} days, "
                  f"Calories: {snack.calories_per_serving}, Comfort: {snack.comfort_factor}/5)")
        print("----------------------------------------")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure 'data/snacks.json' exists in the 'data' directory.")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing snack data: {e}")
        print("Please check the format of 'data/snacks.json'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
