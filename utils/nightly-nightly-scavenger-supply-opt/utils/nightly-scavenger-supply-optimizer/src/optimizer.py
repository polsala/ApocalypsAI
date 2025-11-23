import json

def load_item_manifest(filepath):
    """
    Loads a list of available items from a JSON manifest file.
    Each item should have 'name', 'weight', and 'value' keys.
    """
    with open(filepath, 'r') as f:
        return json.load(f)

def optimize_haul(available_items, max_capacity):
    """
    Optimizes a scavenger's haul given a list of available items and a max capacity.
    Items are prioritized by their value-to-weight ratio.

    Args:
        available_items (list): A list of dictionaries, each with 'name', 'weight', and 'value'.
                                Example: [{'name': 'Water Bottle', 'weight': 1.1, 'value': 10}]
        max_capacity (float): The maximum total weight (or volume) that can be carried.

    Returns:
        tuple: A tuple containing:
            - list: The list of selected items (dictionaries).
            - float: The total weight of the selected items.
            - float: The total value of the selected items.
    """
    if not available_items or max_capacity <= 0:
        return [], 0.0, 0.0

    # Calculate value-to-weight ratio and sort items in descending order
    sorted_items = sorted(
        available_items,
        key=lambda item: (item['value'] / item['weight']) if item['weight'] > 0 else float('inf'),
        reverse=True
    )

    selected_items = []
    current_weight = 0.0
    current_value = 0.0

    for item in sorted_items:
        if current_weight + item['weight'] <= max_capacity:
            selected_items.append(item)
            current_weight += item['weight']
            current_value += item['value']
        # If the item is too heavy on its own, or doesn't fit, skip it.
        # This is a simple greedy approach, not a true knapsack solver.

    return selected_items, current_weight, current_value

def main():
    """
    Example usage of the optimizer.
    """
    print("--- Scavenger's Supply List Optimizer ---")

    # Example manifest (could be loaded from a file)
    example_manifest = [
        {'name': 'Canned Beans', 'weight': 0.5, 'value': 5},
        {'name': 'Water Filter', 'weight': 0.2, 'value': 20},
        {'name': 'First Aid Kit', 'weight': 1.0, 'value': 15},
        {'name': 'Machete', 'weight': 1.5, 'value': 12},
        {'name': 'Radio', 'weight': 0.8, 'value': 8},
        {'name': 'Rope (10m)', 'weight': 0.7, 'value': 7},
        {'name': 'Flashlight', 'weight': 0.3, 'value': 6},
        {'name': 'Extra Batteries', 'weight': 0.1, 'value': 3},
        {'name': 'Map', 'weight': 0.1, 'value': 4},
        {'name': 'Tent', 'weight': 3.0, 'value': 25},
    ]

    max_capacity = 3.0 # kg or arbitrary units

    print(f"\nAvailable items (simulated manifest):")
    for item in example_manifest:
        print(f"  - {item['name']} (Weight: {item['weight']} | Value: {item['value']})")

    print(f"\nMaximum carrying capacity: {max_capacity} units")

    selected_items, total_weight, total_value = optimize_haul(example_manifest, max_capacity)

    print(f"\n--- Optimized Haul ---")
    if selected_items:
        for item in selected_items:
            print(f"  - {item['name']} (Weight: {item['weight']} | Value: {item['value']})")
        print(f"\nTotal Weight: {total_weight:.2f} units")
        print(f"Total Value: {total_value:.2f}")
    else:
        print("No items could be selected within the given capacity.")

if __name__ == '__main__':
    main()
