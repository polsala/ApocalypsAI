# Scavenger Inventory Optimizer

## 🎒 Maximizing Your Haul in the Wasteland 🎒

The ApocalypsAI Nightly Integrator proudly presents the **Scavenger Inventory Optimizer**! In a world where every kilogram counts and every shiny trinket could mean the difference between survival and becoming irradiated dust, this utility is your best friend.

Are you a seasoned wasteland wanderer, a rookie raider, or just someone trying to fit all their precious junk into a rusty backpack? This tool helps you decide which items to carry to maximize your total value, without exceeding your carrying capacity. No more agonizing choices at the abandoned supermarket!

### ✨ Features

*   **Knapsack Algorithm Power**: Leverages a classic dynamic programming approach to find the optimal combination of items.
*   **Value-Driven Selection**: Prioritizes items that give you the most "bang for your buck" (or bottlecap, as it were).
*   **Weight-Conscious**: Ensures you never over-encumber yourself, preventing slow movement or attracting unwanted attention from mutated wildlife.
*   **Self-Contained**: A single Python script, easy to integrate into your post-apocalyptic command line toolkit.

### 🚀 How to Use

1.  **Prepare Your Items**: Create a list of dictionaries, each representing an item you've found. Each item needs:
    *   `name` (string): A unique identifier for the item (e.g., "Rusty Spanner", "Can of Beans (Expired)").
    *   `value` (integer): How valuable the item is to you (e.g., 10 for a rare component, 1 for a piece of scrap).
    *   `weight` (integer): How heavy the item is (e.g., 5 for a heavy weapon, 1 for a small trinket).

2.  **Define Your Capacity**: Determine the maximum total weight you can carry.

3.  **Run the Optimizer**: Call the `optimize_inventory` function with your items and capacity.

#### Example Usage:

```python
from src.optimizer import optimize_inventory

# Your precious haul from the ruins of Sector 7
wasteland_items = [
    {'name': 'Ancient Map to Bunker 42', 'value': 60, 'weight': 10},
    {'name': 'Geiger Counter (slightly broken)', 'value': 100, 'weight': 20},
    {'name': 'Mutant Repellent Spray (half-empty)', 'value': 120, 'weight': 30},
    {'name': 'Shiny Trinket (unknown purpose)', 'value': 10, 'weight': 5},
    {'name': 'Rusty Pipe (makeshift weapon)', 'value': 5, 'weight': 1},
    {'name': 'Can of Nuka-Cola Quantum (flat)', 'value': 25, 'weight': 2},
]

# Your trusty backpack's maximum carrying capacity
backpack_capacity = 50

# Let the optimizer do its magic!
selected_items, total_value, total_weight = optimize_inventory(wasteland_items, backpack_capacity)

print(f"Optimal items for your journey (Capacity: {backpack_capacity}kg):")
for item_name in selected_items:
    print(f"- {item_name}")
print(f"\nTotal Value: {total_value} bottlecaps")
print(f"Total Weight: {total_weight}kg")
```

### 🧪 Testing

To ensure your inventory choices are always optimal, run the included tests:

```bash
python -m unittest tests/test_optimizer.py
```

### 🤝 Contribution

Got a better algorithm for scavenging? Found a bug in the wasteland's physics? Feel free to contribute!
