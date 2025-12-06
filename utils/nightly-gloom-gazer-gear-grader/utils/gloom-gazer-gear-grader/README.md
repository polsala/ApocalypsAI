# Gloom-Gazer Gear Grader

## Overview

In the desolate wastes of the post-apocalypse, every scavenged item counts. The Gloom-Gazer Gear Grader is your trusty companion for evaluating your finds, helping you decide what's truly valuable, what can be salvaged, and what's just more rubble. This utility applies a set of predefined grading rules to a list of items, assigning a 'survival score' to each.

## Features

*   **Item Evaluation**: Calculates a 'survival score' for each item based on its type, condition, rarity, and other attributes.
*   **Configurable Rules**: Grading criteria are defined in a simple JSON configuration file, allowing for easy customization.
*   **Clear Output**: Presents a sorted list of items with their scores, making inventory management a breeze.

## Usage

1.  **Prepare your item list**: Create a JSON file (e.g., `items.json`) containing your scavenged items. Each item should be an object with properties like `name`, `type`, `condition`, `rarity`, and `weight_kg`.

    ```json
    [
      {
        "name": "Rusty Crowbar",
        "type": "weapon",
        "condition": "damaged",
        "rarity": "common",
        "weight_kg": 2.5
      },
      {
        "name": "Sealed MRE (Beef Stew)",
        "type": "food",
        "condition": "new",
        "rarity": "uncommon",
        "weight_kg": 0.4
      }
    ]
    ```

2.  **Define grading rules**: (Optional) Modify `config/grading_rules.json` to suit your survival priorities. The default rules provide a good starting point.

3.  **Run the grader**:

    ```bash
    python3 src/grader.py --items items.json
    ```

    To use custom rules:

    ```bash
    python3 src/grader.py --items items.json --rules config/my_custom_rules.json
    ```

    The utility will print the graded items to standard output, sorted by their survival score.

## Configuration (`config/grading_rules.json`)

The `grading_rules.json` file defines how items are scored. It includes sections for `type_scores`, `condition_scores`, `rarity_scores`, and `weight_penalties`.

```json
{
  "type_scores": {
    "weapon": 10,
    "tool": 8,
    "food": 7,
    "medicine": 12,
    "clothing": 5,
    "junk": -5
  },
  "condition_scores": {
    "new": 5,
    "used": 2,
    "damaged": -3,
    "broken": -10
  },
  "rarity_scores": {
    "rare": 10,
    "uncommon": 5,
    "common": 1,
    "legendary": 20
  },
  "weight_penalties": [
    {"threshold": 5, "penalty": -2},  // -2 points for items >= 5kg
    {"threshold": 10, "penalty": -5} // -5 points for items >= 10kg
  ],
  "missing_attribute_penalty": -1
}
```

## Development

To run tests:

```bash
python3 -m pytest tests/
```
