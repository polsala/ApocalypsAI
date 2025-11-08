# Survival Snack Sorter

## Organize Your Post-Apocalyptic Pantry!

In the grim future, every can counts! The Survival Snack Sorter is a simple command-line utility designed to help you keep track of your vital provisions. Sort your inventory by expiration date to prioritize consumption, or by category to quickly find what you need when the raiders come knocking.

### Features

*   **Expiration-Date Sorting**: Never let a perfectly good MRE go bad again!
*   **Category Sorting**: Group your food, medical supplies, and water for quick access.
*   **Simple CSV Input**: Easy to manage your inventory list.

### Usage

1.  **Prepare your inventory file**: Create a text file (e.g., `inventory.txt`) where each line represents an item with the format: `Item Name,YYYY-MM-DD,Category,Quantity`.

    Example `inventory.txt`:
    ```
    Canned Beans,2025-12-31,Food,10
    Water Bottle,2030-01-01,Drink,5
    First Aid Kit,2024-06-15,Medical,1
    MRE,2026-03-20,Food,7
    Bandages,2024-09-01,Medical,20
    ```

2.  **Run the sorter**:

    ```bash
    python src/sorter.py --file inventory.txt --sort-by expiration
    # or
    python src/sorter.py --file inventory.txt --sort-by category
    ```

### Example Output (sorted by expiration)

```
--- Survival Inventory (Sorted by Expiration) ---

Item Name           Expiration  Category  Quantity
--------------------------------------------------
First Aid Kit       2024-06-15  Medical   1
Bandages            2024-09-01  Medical   20
Canned Beans        2025-12-31  Food      10
MRE                 2026-03-20  Food      7
Water Bottle        2030-01-01  Drink     5
```

### Example Output (sorted by category)

```
--- Survival Inventory (Sorted by Category) ---

Item Name           Expiration  Category  Quantity
--------------------------------------------------
Water Bottle        2030-01-01  Drink     5
Canned Beans        2025-12-31  Food      10
MRE                 2026-03-20  Food      7
First Aid Kit       2024-06-15  Medical   1
Bandages            2024-09-01  Medical   20
```
