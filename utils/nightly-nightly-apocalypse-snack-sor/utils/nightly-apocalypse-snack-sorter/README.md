# Nightly Apocalypse Snack Sorter

## Overview
In the grim future of the ApocalypsAI, every calorie counts, and every moment of joy is a treasure. The `nightly-apocalypse-snack-sorter` is a crucial tool for any discerning survivor looking to optimize their dwindling food supplies. This utility helps you manage your survival snacks, sorting them by critical factors like shelf life, caloric density, and even their 'morale-boosting' potential.

Never again wonder if you should eat that ancient chocolate bar or save the canned beans for another decade! This tool will guide your gastronomic decisions in the wasteland.

## Features
- **Load Snack Inventory**: Reads your snack data from a JSON file.
- **Sort by Shelf Life**: Prioritize snacks that are nearing their expiration.
- **Sort by Caloric Density**: Identify the most energy-packed items.
- **Suggest Morale Boosters**: Find snacks that offer the most psychological comfort.

## Usage
1.  **Prepare your `snacks.json` file**: Create a JSON file (e.g., `my_stash.json`) with your snack inventory. Each snack should be an object with `name` (string), `calories_per_serving` (int), `shelf_life_days` (int), and `morale_boost` (int, 1-5).

    Example `my_stash.json`:
    ```json
    [
        {"name": "Canned Beans", "calories_per_serving": 150, "shelf_life_days": 1825, "morale_boost": 2},
        {"name": "Energy Bar", "calories_per_serving": 250, "shelf_life_days": 730, "morale_boost": 4},
        {"name": "Dried Fruit Mix", "calories_per_serving": 100, "shelf_life_days": 365, "morale_boost": 3},
        {"name": "Chocolate Bar", "calories_per_serving": 300, "shelf_life_days": 180, "morale_boost": 5},
        {"name": "MRE (Meal, Ready-to-Eat)", "calories_per_serving": 1200, "shelf_life_days": 1825, "morale_boost": 3}
    ]
    ```

2.  **Run the utility**:

    ```bash
    # Sort by longest shelf life first
    python3 src/snack_sorter.py --file my_stash.json --sort-by shelf_life

    # Sort by highest caloric density first
    python3 src/snack_sorter.py --file my_stash.json --sort-by calories

    # List the top 3 snacks for morale boosting
    python3 src/snack_sorter.py --file my_stash.json --morale-boosters 3
    ```

## Arguments
- `--file <path>`: Path to your `snacks.json` inventory file (required).
- `--sort-by <criteria>`: Sorts snacks. Options: `shelf_life`, `calories`.
- `--morale-boosters <count>`: Lists the top `count` snacks by morale boost.

## Development
This utility is written in Python 3.11 and requires no external dependencies beyond the standard library.

To run tests:
```bash
python3 -m unittest tests/test_snack_sorter.py
```
