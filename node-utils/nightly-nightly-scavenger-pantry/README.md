# Nightly Scavenger Pantry

A whimsical CLI utility to help post‑apocalypse survivors track their pantry items and expiration dates.

## Features

- Add items with a name and days until they expire.
- List all stored items.
- Show items that will expire within the next 7 days.

## Installation

```sh
git clone <repo-url>
cd utils/nightly-scavenger-pantry
npm install
```

(Or just run with Node, no external dependencies.)

## Usage

```sh
node src/cli.js add "Canned Beans" 30
node src/cli.js add "Bottled Water" 365
node src/cli.js list
node src/cli.js check
```

- `add <name> <days>` – stores an item.
- `list` – prints all items.
- `check` – prints items expiring within 7 days.

Data is stored in `data.json` in the utility directory.
