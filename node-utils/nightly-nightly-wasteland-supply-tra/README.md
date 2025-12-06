# nightly‑wasteland‑supply‑tracker

A whimsical yet practical command‑line utility for keeping track of the items in your post‑apocalyptic survival kit.

## Features

- **Add** an item with its weight (kg)
- **Remove** an item by name
- **List** all stored items
- **Total** the combined weight of the kit
- Persists data to a local `inventory.json` file so the list survives between runs.

## Installation

```bash
# Clone the repo (or copy the folder) and install dependencies
npm install
```

> No external dependencies are required – the tool uses only Node's built‑in modules.

## Usage

```bash
node src/main.js add "Water Bottle" 2.5   # add an item
node src/main.js add "First‑Aid Kit" 1.2
node src/main.js list                     # show all items
node src/main.js total                    # total weight in kg
node src/main.js remove "Water Bottle"   # delete an item
```

The inventory is stored in `inventory.json` next to the script.  You can delete this file to reset the kit.

## Testing

```bash
node tests/test_main.js
```

All tests should pass with a clean Node 18+ environment.
