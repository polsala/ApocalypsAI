import argparse
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class GearItem:
    name: str
    weight: float
    base_utility: int
    condition: float = 1.0  # 0.0 to 1.0
    tags: List[str] = field(default_factory=list)

    @property
    def effective_utility(self) -> float:
        """Calculates utility adjusted by condition."""
        return self.base_utility * self.condition

    @property
    def utility_per_weight(self) -> float:
        """Calculates utility per unit of weight, handling zero weight."""
        if self.weight <= 0:
            return float('inf')  # Infinitely useful if it weighs nothing
        return self.effective_utility / self.weight

def load_gear_from_json(file_path: str) -> List[GearItem]:
    """Loads gear items from a JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    gear_list = []
    for item_data in data:
        try:
            gear_list.append(GearItem(
                name=item_data['name'],
                weight=float(item_data['weight']),
                base_utility=int(item_data['base_utility']),
                condition=float(item_data.get('condition', 1.0)),
                tags=item_data.get('tags', [])
            ))
        except (KeyError, ValueError) as e:
            print(f"Warning: Skipping malformed gear item {item_data.get('name', 'unknown')}: {e}")
    return gear_list

def optimize_loadout(
    available_items: List[GearItem],
    max_weight: float,
    task_tags: List[str] = None
) -> List[GearItem]:
    """
    Optimizes a gear loadout based on maximum weight and task-specific tags.
    Uses a greedy approach: prioritizes items with matching tags, then by utility-per-weight.
    """
    if task_tags is None:
        task_tags = []

    # Filter items by task tags if provided
    if task_tags:
        relevant_items = [
            item for item in available_items
            if any(tag in item.tags for tag in task_tags)
        ]
        # If no relevant items, consider all items to still provide a loadout
        if not relevant_items:
            relevant_items = available_items
    else:
        relevant_items = available_items

    # Sort items by utility_per_weight in descending order
    # Items with higher utility_per_weight are preferred
    sorted_items = sorted(relevant_items, key=lambda item: item.utility_per_weight, reverse=True)

    current_loadout: List[GearItem] = []
    current_weight = 0.0

    for item in sorted_items:
        if current_weight + item.weight <= max_weight:
            current_loadout.append(item)
            current_weight += item.weight
    
    return current_loadout

def main():
    parser = argparse.ArgumentParser(
        description="Optimize your post-apocalyptic gear loadout."
    )
    parser.add_argument(
        "--gear-file",
        type=str,
        required=True,
        help="Path to the JSON file containing your gear inventory."
    )
    parser.add_argument(
        "--max-weight",
        type=float,
        required=True,
        help="Your maximum carrying capacity."
    )
    parser.add_argument(
        "--task-tags",
        nargs='*',  # 0 or more arguments
        default=[],
        help="Space-separated list of tags relevant to your current mission (e.g., scavenging combat)."
    )

    args = parser.parse_args()

    available_gear = load_gear_from_json(args.gear_file)
    
    optimized_loadout = optimize_loadout(
        available_gear,
        args.max_weight,
        args.task_tags
    )

    total_weight = sum(item.weight for item in optimized_loadout)
    total_effective_utility = sum(item.effective_utility for item in optimized_loadout)

    print(f"Optimized Loadout for task(s) {args.task_tags} (Max Weight: {args.max_weight}):")
    if not optimized_loadout:
        print("  No items selected. Perhaps increase max weight or adjust task tags?")
    for item in optimized_loadout:
        print(f"- {item.name} (Weight: {item.weight}, Utility: {item.effective_utility:.1f})")
    print(f"Total Weight: {total_weight:.1f}")
    print(f"Total Effective Utility: {total_effective_utility:.1f}")

if __name__ == "__main__":
    main()
