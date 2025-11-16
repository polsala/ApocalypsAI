# Nightly Apocalypse Snack Sorter

A crucial utility for the discerning survivor, the Nightly Apocalypse Snack Sorter helps you manage your precious food supplies by categorizing them into strategic groups. No more guessing which canned good to hoard or which fresh berry to devour immediately!

## Features

*   **Intelligent Categorization**: Sorts food items into:
    *   **Long-Term Survival**: Non-perishable, high-calorie staples for the long haul.
    *   **Short-Term Morale Boost**: Comfort foods and treats to keep spirits high.
    *   **Immediate Consumption**: Perishable items that need to be eaten before they spoil.
*   **Simple CLI Interface**: Easily process a list of items.
*   **Extensible Rules**: The categorization logic is straightforward and can be easily updated.

## Usage

To sort your inventory, provide a list of food items as command-line arguments:

```bash
python src/sorter.py "Canned Beans" "Fresh Apples" "Chocolate Bar" "Rice" "Milk"
```

The utility will output the categorized list:

```
--- Apocalypse Snack Inventory ---
Long-Term Survival:
  - Canned Beans
  - Rice
Short-Term Morale Boost:
  - Chocolate Bar
Immediate Consumption:
  - Fresh Apples
  - Milk
```

## Development

### Running Tests

To ensure the sorter is functioning correctly, run the tests:

```bash
python -m unittest tests/test_sorter.py
```

### Customizing Categories

The categorization rules are defined within `src/sorter.py`. You can modify the `CATEGORIES` dictionary and the `categorize_item` function to suit your specific post-apocalyptic dietary needs.
