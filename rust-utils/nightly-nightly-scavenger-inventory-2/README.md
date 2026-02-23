# nightly-scavenger-inventory

A whimsical CLI tool for post‑apocalypse scavengers to manage their inventory of supplies. It reads a JSON file of items (name, quantity, expiration date) and can list items sorted by soonest expiration, warn about expired items, and add new items.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
# List items (sorted, with warnings)
nightly-scavenger-inventory list inventory.json

# Add a new item
nightly-scavenger-inventory add inventory.json "Canned Beans" 12 2025-12-31
```

The inventory file format:

```json
[
  {"name":"Water Bottle","quantity":5,"expires":"2024-05-01"},
  {"name":"Energy Bar","quantity":10,"expires":"2023-11-15"}
]
```

## License

MIT
