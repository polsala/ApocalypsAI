# Nightly Gloom-Gazer Gear Grader

## Overview

In the grim twilight of the apocalypse, every piece of gear counts. The Gloom-Gazer Gear Grader is your trusty companion for assessing the state of your precious equipment. This utility helps you prioritize repairs, identify critical failures, and keep your inventory in fighting shape, ensuring you're always ready for whatever the wasteland throws at you.

## Features

*   **Condition-based Grading**: Assigns a priority level (CRITICAL, URGENT, MAINTAIN, GOOD, MISC) based on an item's condition score and type.
*   **Configurable Gear Types**: Easily extendable to include new categories of items (default essential types: `weapon`, `armor`, `tool`).
*   **Simple CLI Interface**: Process your gear list from a text file and get an organized report.

## Usage

1.  **Prepare your gear list**: Create a text file (e.g., `gear.txt`) where each line represents an item in the format:
    `Item Name,Type,Condition Score`

    Example `gear.txt`:
    ```
    Rusty Machete,weapon,35
    Makeshift Armor Vest,armor,60
    Water Purifier,tool,15
    First Aid Kit,consumable,90
    Broken Radio,misc,5
    Hunting Rifle,weapon,85
    ```

2.  **Run the grader**: From the `utils/nightly-gloom-gazer-gear-grader/` directory, execute:
    ```bash
    python src/grader.py gear.txt
    ```

## Output Example

```
--- Gear Grading Report ---

CRITICAL (Requires immediate attention!):
  - Water Purifier (tool) - Condition: 15/100

URGENT (Needs repair soon):
  - Rusty Machete (weapon) - Condition: 35/100

MAINTAIN (Keep an eye on it):
  - Makeshift Armor Vest (armor) - Condition: 60/100

GOOD (Ready for action!):
  - First Aid Kit (consumable) - Condition: 90/100
  - Hunting Rifle (weapon) - Condition: 85/100

MISC (Non-essential, low priority):
  - Broken Radio (misc) - Condition: 5/100
```

## Development

The `grader.py` script is written in Python 3.11 and is self-contained. Tests are located in `tests/test_grader.py`.

To run tests:
```bash
python -m unittest tests/test_grader.py
```
