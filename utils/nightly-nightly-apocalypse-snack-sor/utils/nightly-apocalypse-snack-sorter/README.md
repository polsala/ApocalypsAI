# Nightly Apocalypse Snack Sorter

## Overview
In the grim reality of a post-apocalyptic world, every bite counts. The 'Nightly Apocalypse Snack Sorter' is a crucial utility designed to help survivors manage their precious food supplies. It takes a list of available snacks and intelligently sorts them based on a combination of shelf-life, nutritional value, and a morale-boosting 'comfort factor'. Never again will you accidentally let that last can of beans expire while hoarding your favorite chocolate bar!

## Features
- **Intelligent Prioritization**: Sorts snacks by shortest shelf-life first, then by highest caloric content, and finally by highest comfort factor.
- **Customizable Data**: Easily add or modify snack entries in the `data/snacks.json` file.
- **Simple CLI**: Run directly from your terminal to get an immediate consumption plan.

## Usage

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/nightly-apocalypse-snack-sorter
    ```

2.  **Run the sorter**:
    ```bash
    python src/snack_sorter.py
    ```

    The utility will print a prioritized list of snacks to your console.

## Data Format (`data/snacks.json`)

The `snacks.json` file should be a JSON array of objects, where each object represents a snack with the following keys:

-   `name` (string): The name of the snack (e.g., "Canned Beans", "Chocolate Bar").
-   `shelf_life_days` (integer): Remaining shelf life in days. Lower values are prioritized.
-   `calories_per_serving` (integer): Calories per serving. Higher values are prioritized.
-   `comfort_factor` (integer, 1-5): A subjective rating of how much comfort or morale the snack provides. 5 is highest comfort. Higher values are prioritized.

**Example `data/snacks.json`:**
```json
[
  {
    "name": "Canned Beans",
    "shelf_life_days": 365,
    "calories_per_serving": 200,
    "comfort_factor": 2
  },
  {
    "name": "MRE (Meal, Ready-to-Eat)",
    "shelf_life_days": 730,
    "calories_per_serving": 1200,
    "comfort_factor": 3
  },
  {
    "name": "Chocolate Bar",
    "shelf_life_days": 90,
    "calories_per_serving": 250,
    "comfort_factor": 5
  },
  {
    "name": "Dried Fruit",
    "shelf_life_days": 180,
    "calories_per_serving": 150,
    "comfort_factor": 3
  }
]
```

## Development

To run tests:
```bash
python -m unittest tests/test_snack_sorter.py
```
