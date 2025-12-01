# Nightly Apocalypse Snack Sorter

A Python CLI utility designed to help you organize your emergency food supply. It sorts your pantry items based on their estimated shelf life and nutritional value, providing a prioritized list of what to consume first to minimize waste and maximize survival efficiency.

## How to Use

1.  **Prepare your inventory CSV file.** Create a file named `inventory.csv` (or any other name) with the following columns: `item_name`, `shelf_life_days`, `calories_per_serving`, `servings`.
    *   `item_name`: (string) The name of the food item (e.g., "Canned Beans", "Energy Bar").
    *   `shelf_life_days`: (integer) The estimated number of days until the item expires or significantly degrades in quality.
    *   `calories_per_serving`: (integer) The number of calories per single serving.
    *   `servings`: (integer) The total number of servings available for this item.

    **Example `inventory.csv`:**
    ```csv
    Canned Tuna,365,150,2
    Protein Bar,90,250,1
    Bottled Water,730,0,10
    MRE,1825,1200,1
    Crackers,60,100,5
    ```

2.  **Run the sorter.** Execute the script with your CSV file as an argument:

    ```bash
    python src/sorter.py inventory.csv
    ```

3.  **Review the prioritized list.** The utility will print a table of your items, sorted by consumption priority (highest priority first).

## Output Example

```
Apocalypse Snack Sorter - Prioritized Consumption List

+-----------------+-------------------+-----------------------+----------+------------------+
| Item Name       | Shelf Life (Days) | Calories (Total)      | Servings | Priority Score   |
+-----------------+-------------------+-----------------------+----------+------------------+
| Crackers        | 60                | 500                   | 5        | 55.00            |
| Protein Bar     | 90                | 250                   | 1        | 87.50            |
| Canned Tuna     | 365               | 300                   | 2        | 362.00           |
| Bottled Water   | 730               | 0                     | 10       | 730.00           |
| MRE             | 1825              | 1200                  | 1        | 1813.00          |
+-----------------+-------------------+-----------------------+----------+------------------+

*Lower Priority Score indicates higher consumption priority.*
```

## How Priority is Calculated

The priority score is calculated using a simple heuristic:
`Priority Score = (shelf_life_days * 1) - (calories_per_serving * servings * 0.01)`

*   Items with **shorter shelf lives** get a lower score (higher priority).
*   Items with **more total calories** (calories_per_serving * servings) get a lower score (higher priority).

This ensures that items expiring sooner and those providing more energy are prioritized for consumption.
