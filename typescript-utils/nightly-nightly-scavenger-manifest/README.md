# Nightly Scavenger Manifest

A type-safe CLI tool for survivors to meticulously track their scavenged items, their current condition, and potential uses within a digital manifest. No more losing track of that 'slightly glowing' wrench or the 'rust-kissed' can of beans!

## Features

*   **Type-Safe Item Management**: Define and manage items with strict types for name, category, condition, quantity, and notes.
*   **Condition Tracking**: Keep tabs on the wear and tear of your gear with predefined conditions like 'Pristine', 'Worn', 'Broken', and 'Mysterious'.
*   **Search & Filter**: Quickly find items by name, category, or condition.
*   **Persistent Storage**: Your manifest is saved to a JSON file, so your precious loot is never forgotten.

## Installation

1.  Navigate to the `nightly-scavenger-manifest` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## Usage

The utility operates via a command-line interface. All data is stored in `manifest.json` in the current directory.

### Add an Item

```bash
./bin/scavenger-manifest add --name "Rusty Spanner" --category "Tool" --condition "Worn" --quantity 1 --notes "Good for loosening stubborn bolts."
./bin/scavenger-manifest add --name "Can of Mystery Meat" --category "Food" --condition "Mysterious" --quantity 3 --notes "Expiration date long gone, but still sealed."
```

### List All Items

```bash
./bin/scavenger-manifest list
```

### Update an Item

Requires the item's ID (found via `list`).

```bash
./bin/scavenger-manifest update --id <item-id> --condition "Broken" --notes "Handle snapped off."
```

### Remove an Item

Requires the item's ID.

```bash
./bin/scavenger-manifest remove --id <item-id>
```

### Search Items

Search by name, category, or condition. Case-insensitive.

```bash
./bin/scavenger-manifest search --query "tool"
./bin/scavenger-manifest search --category "food"
./bin/scavenger-manifest search --condition "mysterious"
```

## Development

To run tests:

```bash
npm test
```

To run directly with `ts-node` (for development):

```bash
npx ts-node src/index.ts add --name "Dev Item" --category "Test" --condition "Pristine" --quantity 1
```
