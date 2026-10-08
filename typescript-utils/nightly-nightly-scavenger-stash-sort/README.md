# Nightly Scavenger's Stash Sorter

A type-safe TypeScript CLI utility to help post-apocalyptic scavengers (or anyone with a messy inventory) sort their found items into predefined stash categories based on custom rules and priorities.

## Features

*   **Type-Safe Item & Category Definitions**: Define your items and stash categories with clear types.
*   **Rule-Based Sorting**: Assign items to categories using flexible, user-defined rules (e.g., by type, value, weight).
*   **Priority-Driven Assignment**: Categories can have priorities, ensuring items land in the most appropriate stash if multiple rules match.
*   **CLI Interface**: Easily sort items from a JSON input file.

## Installation

1.  Ensure you have Node.js and npm/yarn installed.
2.  Navigate to the utility's directory:
    ```bash
    cd typescript-utils/nightly-scavenger-stash-sorter
    ```
3.  Install dependencies:
    ```bash
    npm install
    # or yarn install
    ```
4.  Build the TypeScript project:
    ```bash
    npm run build
    # or yarn build
    ```

## Usage

1.  Create an `items.json` file (or any `.json` file) containing an array of items you want to sort. Each item should conform to the `Item` interface:

    ```json
    // items.json
    [
      { "name": "Rusty Can Opener", "type": "Tool", "weight": 0.5, "volume": 0.1, "value": 5 },
      { "name": "Purified Water Bottle", "type": "Water", "weight": 1.0, "volume": 1.0, "value": 20 },
      { "name": "Moldy Bread", "type": "Food", "weight": 0.2, "volume": 0.2, "value": 2 },
      { "name": "Pre-War Comic Book", "type": "Relic", "weight": 0.1, "volume": 0.05, "value": 150 },
      { "name": "Scrap Metal (x10)", "type": "Component", "weight": 2.0, "volume": 0.5, "value": 10 },
      { "name": "Broken Goggles", "type": "Junk", "weight": 0.1, "volume": 0.1, "value": 1 }
    ]
    ```

2.  (Optional) Customize `src/categories.ts` to define your own `StashCategory` rules and priorities. The default categories are:
    *   `Survival Essentials`: High priority, for food, water, critical tools.
    *   `Tradeable Trinkets`: Medium priority, for valuable relics or components.
    *   `Curious Collectibles`: Lower priority, for unique but not immediately useful items.
    *   `Scrap & Salvage`: Lowest priority, for junk and basic components.

3.  Run the sorter, providing the path to your items JSON file:

    ```bash
    npm start -- items.json
    # or yarn start items.json
    ```

    The output will be a JSON object where keys are category names and values are arrays of items assigned to that category.

    Example Output:
    ```json
    {
      "Survival Essentials": [
        { "name": "Purified Water Bottle", "type": "Water", "weight": 1, "volume": 1, "value": 20 },
        { "name": "Moldy Bread", "type": "Food", "weight": 0.2, "volume": 0.2, "value": 2 },
        { "name": "Rusty Can Opener", "type": "Tool", "weight": 0.5, "volume": 0.1, "value": 5 }
      ],
      "Tradeable Trinkets": [
        { "name": "Pre-War Comic Book", "type": "Relic", "weight": 0.1, "volume": 0.05, "value": 150 }
      ],
      "Curious Collectibles": [],
      "Scrap & Salvage": [
        { "name": "Scrap Metal (x10)", "type": "Component", "weight": 2, "volume": 0.5, "value": 10 },
        { "name": "Broken Goggles", "type": "Junk", "weight": 0.1, "volume": 0.1, "value": 1 }
      ]
    }
    ```

## Development

To run tests:

```bash
npm test
# or yarn test
```
