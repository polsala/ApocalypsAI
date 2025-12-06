# Scavenger's Supply List Optimizer

## Overview

In the desolate wastes, every ounce of carrying capacity counts. The `nightly-scavenger-supply-optimizer` is a crucial tool for any discerning survivor, helping you make tough choices about what to haul back to your shelter. This utility takes a list of available items (each with a weight and a perceived value) and your maximum carrying capacity, then calculates the optimal set of items to maximize your total utility.

It's not just for the apocalypse! Use it to pack for a camping trip, optimize your grocery run, or decide what to keep when decluttering.

## How it Works

The optimizer employs a greedy algorithm: it prioritizes items with the highest 'value-to-weight' ratio. This ensures that you're getting the most bang for your buck (or, more accurately, the most utility for your bulk).

## Usage

1.  **Prepare your item manifest**: Create a JSON file (e.g., `manifest.json`) containing a list of dictionaries. Each dictionary should represent an item and have the following keys:
    *   `name` (string): The name of the item.
    *   `weight` (float): The weight or volume of the item (e.g., in kg, liters, or arbitrary units).
    *   `value` (float): Your subjective utility score for the item (higher is better).

    Example `manifest.json`:
    ```json
    [
      {"name": "Canned Beans", "weight": 0.5, "value": 5},
      {"name": "Water Filter", "weight": 0.2, "value": 20},
      {"name": "First Aid Kit", "weight": 1.0, "value": 15},
      {"name": "Machete", "weight": 1.5, "value": 12}
    ]
    ```

2.  **Run the optimizer**: Execute the `optimizer.py` script, optionally modifying the `main()` function to load your specific manifest and set your `max_capacity`.

    ```bash
    python3 src/optimizer.py
    ```

    The script will print the optimized list of items, their total weight, and total value.

## Example Output

```
--- Scavenger's Supply List Optimizer ---

Available items (simulated manifest):
  - Canned Beans (Weight: 0.5 | Value: 5)
  - Water Filter (Weight: 0.2 | Value: 20)
  - First Aid Kit (Weight: 1.0 | Value: 15)
  - Machete (Weight: 1.5 | Value: 12)
  - Radio (Weight: 0.8 | Value: 8)
  - Rope (10m) (Weight: 0.7 | Value: 7)
  - Flashlight (Weight: 0.3 | Value: 6)
  - Extra Batteries (Weight: 0.1 | Value: 3)
  - Map (Weight: 0.1 | Value: 4)
  - Tent (Weight: 3.0 | Value: 25)

Maximum carrying capacity: 3.0 units

--- Optimized Haul ---
  - Water Filter (Weight: 0.2 | Value: 20)
  - First Aid Kit (Weight: 1.0 | Value: 15)
  - Machete (Weight: 1.5 | Value: 12)
  - Flashlight (Weight: 0.3 | Value: 6)

Total Weight: 3.00 units
Total Value: 53.00
```
