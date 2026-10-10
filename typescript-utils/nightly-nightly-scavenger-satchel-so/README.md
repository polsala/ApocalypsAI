# Nightly Scavenger's Satchel Sorter

## Overview

The `nightly-scavenger-satchel-sorter` is a whimsical-yet-useful TypeScript CLI utility designed to assist survivors in the wasteland. It helps you decide which precious items to carry in your satchel by optimizing for 'survival score' while respecting your satchel's maximum weight and volume capacities. Think of it as a post-apocalyptic knapsack problem solver!

## Features

*   **Item Prioritization**: Sorts items based on a calculated priority (survival score, then density).
*   **Capacity Constraints**: Respects both maximum weight and maximum volume limits.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.
*   **CLI Interface**: Easy to use from your terminal.

## Installation

To use this utility, you need Node.js (which includes npm or yarn) and TypeScript installed.

1.  Navigate to the utility's directory:
    ```bash
    cd nightly-scavenger-satchel-sorter
    ```
2.  Install dependencies:
    ```bash
    npm install
    # or yarn install
    ```
3.  Build the TypeScript project (optional, `ts-node` can run directly):
    ```bash
    npm run build
    ```

## Usage

Run the utility using `ts-node` (for direct execution) or after building (for compiled JS).

```bash
npm start -- --items-file <path-to-items.json> --max-weight <number> --max-volume <number>
# Example:
npm start -- --items-file sample-items.json --max-weight 5.0 --max-volume 3.0
```

### Arguments:

*   `--items-file <path>`: **(Required)** Path to a JSON file containing an array of item objects. See `sample-items.json` for format.
*   `--max-weight <number>`: **(Required)** The maximum weight capacity of your satchel (e.g., in kilograms).
*   `--max-volume <number>`: **(Required)** The maximum volume capacity of your satchel (e.g., in liters).

### `items.json` Format Example:

The `items-file` should be a JSON array where each object represents an item with the following properties:

```json
[
  {
    "name": "Water Bottle (full)",
    "weight": 1.1,      // in kg
    "volume": 1.0,      // in liters
    "survival_score": 100 // arbitrary points, higher is better
  },
  {
    "name": "Canned Beans (x2)",
    "weight": 0.8,
    "volume": 0.6,
    "survival_score": 100
  }
]
```

## Example Output

```
--- Scavenger's Satchel Report ---
Max Capacity: 5.0kg, 3.0L

Selected Items:
  - Sleeping Bag (compact) (Score: 150, W: 1.2kg, V: 2.0L)
  - First Aid Kit (basic) (Score: 120, W: 0.8kg, V: 0.5L)
  - Water Bottle (full) (Score: 100, W: 1.1kg, V: 1.0L)
  - Flashlight (LED) (Score: 55, W: 0.3kg, V: 0.15L)

Summary:
  Total Weight: 3.40kg
  Total Volume: 3.65L
  Total Survival Score: 425
```

*(Note: The example output above is illustrative. Actual output will depend on your item list and capacities.)*

## Development

### Running Tests

```bash
npm test
```

### Linting and Formatting

```bash
npm run lint
npm run format
```
