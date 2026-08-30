# nightly-stash-sorter

A whimsical-yet-useful type-safe CLI tool for the discerning scavenger, designed to help organize and prioritize your scavenged items based on customizable survival criteria. No more rummaging through your backpack in the dark!

## Features

*   **Type-Safe Item Management**: Define your scavenged items with clear types for `category`, `rarity`, `condition`, `weight`, and `value`.
*   **Flexible Filtering**: Filter items by category, rarity, or minimum condition.
*   **Customizable Sorting**: Sort your stash by any item property (e.g., `value_units`, `weight_kg`, `condition`, `name`) in ascending or descending order.
*   **Result Limiting**: Focus on your most critical items by limiting the output.
*   **CLI Interface**: Easily integrate into your nightly routines or shell scripts.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-stash-sorter
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Build the project:**
    ```bash
    npm run build
    ```
4.  **(Optional) Link the CLI tool globally:**
    ```bash
    npm link
    # Now you can run 'stash-sorter' from anywhere
    ```

## Usage

The `stash-sorter` command takes an input JSON file containing your scavenged items and applies sorting and filtering rules.

### Input File Format (e.g., `my_stash.json`)

Your input file should be a JSON array of `ScavengedItem` objects:

```json
[
  {
    "id": "item-001",
    "name": "Canned Peaches",
    "category": "food",
    "rarity": "common",
    "condition": "good",
    "weight_kg": 0.4,
    "value_units": 12,
    "perishable": false
  },
  {
    "id": "item-002",
    "name": "Hunting Rifle",
    "category": "weapon",
    "rarity": "rare",
    "condition": "worn",
    "weight_kg": 3.5,
    "value_units": 75
  },
  {
    "id": "item-003",
    "name": "Dirty Water",
    "category": "water",
    "rarity": "common",
    "condition": "damaged",
    "weight_kg": 1.1,
    "value_units": 3,
    "perishable": true
  }
]
```

### Command Line Arguments

```bash
stash-sorter sort <input-file> [output-file] [options]
```

**Options:**

*   `--category <cat1,cat2,...>`: Filter by item categories (e.g., `food,weapon,medical`).
    *   Available categories: `food`, `water`, `tool`, `weapon`, `medical`, `misc`.
*   `--rarity <rar1,rar2,...>`: Filter by item rarities (e.g., `common,rare`).
    *   Available rarities: `common`, `uncommon`, `rare`, `legendary`.
*   `--min-condition <condition>`: Filter by minimum condition. Items with a condition equal to or better than the specified one will be included.
    *   Condition order (worst to best): `broken`, `damaged`, `worn`, `good`, `pristine`.
*   `--sort-by <field>`: Sort the results by a specific item field.
    *   Available fields: `id`, `name`, `category`, `rarity`, `condition`, `weight_kg`, `value_units`.
*   `--sort-order <order>`: Specify sort order (`asc` for ascending, `desc` for descending). Default is `asc`.
*   `--limit <number>`: Limit the number of items in the output.

### Examples

1.  **Sort all items by value, descending, and output to console:**
    ```bash
    stash-sorter sort my_stash.json --sort-by value_units --sort-order desc
    ```

2.  **Find the 5 most valuable 'food' or 'medical' items in 'good' or better condition:**
    ```bash
    stash-sorter sort my_stash.json --category food,medical --min-condition good --sort-by value_units --sort-order desc --limit 5
    ```

3.  **List all 'rare' weapons, sorted by weight (ascending), and save to a new file:**
    ```bash
    stash-sorter sort my_stash.json sorted_weapons.json --category weapon --rarity rare --sort-by weight_kg
    ```

## Development

To run tests:
```bash
npm test
```

To run the CLI directly with `ts-node` (without building):
```bash
npm start -- sort my_stash.json --sort-by name
```

## License

This project is licensed under the MIT License.
