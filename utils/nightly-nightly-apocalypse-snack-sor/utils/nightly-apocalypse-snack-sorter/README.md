# Nightly Apocalypse Snack Sorter

## Overview

In the grim darkness of the far future (or just a power outage), knowing what's in your pantry and how long it'll last, or how much joy it'll bring, is crucial. The `Nightly Apocalypse Snack Sorter` is a whimsical-yet-useful utility designed to help you categorize your food items. It sorts them into 'Shelf Stability' (Long-Haul, Mid-Term, Perishable Panic, Unknown Stability) and 'Comfort Level' (Soul Soother, Morale Booster, Pure Sustenance) categories.

Prepare your bunker, one snack at a time!

## Usage

1.  **Create an input file**: Create a plain text file (e.g., `snacks.txt`) where each line is a food item you want to sort.

    Example `snacks.txt`:
    ```
    Canned Beans
    Fresh Apples
    Chocolate Bar
    Rice
    Milk
    Chips
    Dried Mango
    Coffee
    Bread
    Water
    ```

2.  **Run the sorter**: Execute the `sorter.py` script with your input file.

    ```bash
    python3 src/sorter.py snacks.txt
    ```

3.  **Review the report**: The script will print a categorized report to your console.

## Example Output

```
Apocalypse Snack Sorter Report:

--- Canned Beans ---
  Shelf Stability: Long-Haul
  Comfort Level: Pure Sustenance

--- Fresh Apples ---
  Shelf Stability: Perishable Panic
  Comfort Level: Pure Sustenance

--- Chocolate Bar ---
  Shelf Stability: Mid-Term
  Comfort Level: Soul Soother

--- Rice ---
  Shelf Stability: Long-Haul
  Comfort Level: Pure Sustenance

--- Milk ---
  Shelf Stability: Perishable Panic
  Comfort Level: Pure Sustenance

--- Chips ---
  Shelf Stability: Mid-Term
  Comfort Level: Morale Booster

--- Dried Mango ---
  Shelf Stability: Long-Haul
  Comfort Level: Pure Sustenance

--- Coffee ---
  Shelf Stability: Mid-Term
  Comfort Level: Soul Soother

--- Bread ---
  Shelf Stability: Perishable Panic
  Comfort Level: Pure Sustenance

--- Water ---
  Shelf Stability: Unknown Stability
  Comfort Level: Pure Sustenance
```

## Development

This utility is written in Python 3.11 and has no external dependencies beyond the standard library.

## Tests

To run the tests, navigate to the `tests/` directory and execute:

```bash
python3 -m unittest test_sorter.py
```
