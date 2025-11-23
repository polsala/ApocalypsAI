import sys
from dataclasses import dataclass
from typing import List

@dataclass
class Snack:
    name: str
    shelf_life_days: int
    calories: int
    comfort_score: int

    def __lt__(self, other): # For sorting
        # Primary sort: shortest shelf life first
        if self.shelf_life_days != other.shelf_life_days:
            return self.shelf_life_days < other.shelf_life_days
        # Secondary sort: highest calories first (descending)
        if self.calories != other.calories:
            return self.calories > other.calories
        # Tertiary sort: highest comfort score first (descending)
        return self.comfort_score > other.comfort_score

def parse_snacks_from_file(filepath: str) -> List[Snack]:
    """
    Parses snack data from a given file path.
    Each line should be: Snack Name,Shelf Life (days),Calories,Comfort Score (1-5)
    """
    snacks = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): # Skip empty lines or comments
                    continue
                parts = line.split(',')
                if len(parts) == 4:
                    try:
                        name = parts[0].strip()
                        shelf_life = int(parts[1].strip())
                        calories = int(parts[2].strip())
                        comfort = int(parts[3].strip())
                        if not (1 <= comfort <= 5):
                            print(f"Warning: Comfort score for '{name}' out of range (1-5). Skipping.", file=sys.stderr)
                            continue
                        snacks.append(Snack(name, shelf_life, calories, comfort))
                    except ValueError:
                        print(f"Warning: Could not parse line: '{line}'. Skipping.", file=sys.stderr)
                else:
                    print(f"Warning: Incorrect format for line: '{line}'. Skipping.", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'", file=sys.stderr)
        sys.exit(1)
    return snacks

def sort_snacks(snacks: List[Snack]) -> List[Snack]:
    """Sorts snacks based on shelf life, calories, and comfort score."""
    return sorted(snacks)

def print_prioritized_snacks(snacks: List[Snack]):
    """Prints the sorted list of snacks with consumption recommendations."""
    print("\n--- Apocalypse Snack Prioritization ---\n")
    for i, snack in enumerate(snacks):
        recommendation = "- Consume Soon!" if i < 2 else "- Store for Later."
        if snack.shelf_life_days <= 30: # More aggressive 'consume soon' for very short shelf life
            recommendation = "- **CRITICAL: CONSUME IMMEDIATELY!**"
        elif snack.shelf_life_days <= 90 and i > 1:
             recommendation = "- Consume Soon!"

        print(f"{i+1}. {snack.name} (Shelf Life: {snack.shelf_life_days} days, Calories: {snack.calories}, Comfort: {snack.comfort_score}) {recommendation}")
    print("\n--- Stay Fed, Stay Alive! ---\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 sorter.py <path_to_snack_file.txt>", file=sys.stderr)
        sys.exit(1)

    snack_filepath = sys.argv[1]
    raw_snacks = parse_snacks_from_file(snack_filepath)
    if not raw_snacks:
        print("No valid snacks found to sort.", file=sys.stderr)
        sys.exit(0)

    prioritized_snacks = sort_snacks(raw_snacks)
    print_prioritized_snacks(prioritized_snacks)
