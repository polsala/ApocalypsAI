# nightly‑scavenger‑inventory

A tiny Rust command‑line utility for the post‑apocalyptic wanderer who wants to keep track of scavenged food, water, and supplies.

## Features

- Store items (name, quantity, days‑until‑expiration) in a local JSON file.
- Add new items via `add` sub‑command.
- List all items sorted by expiration.
- Suggest the item that should be consumed next (the one that expires soonest).

## Installation

```bash
# Ensure you have Rust toolchain installed (rustc + cargo)
cargo install --path .
```

## Usage

The inventory is stored in `inventory.json` in the current working directory.

```bash
# Add an item
nightly-scavenger-inventory add --name "Canned Beans" --quantity 4 --expires 365

# List items (sorted by expiration)
nightly-scavenger-inventory list

# Get a suggestion for what to eat/drink first
nightly-scavenger-inventory suggest
```

## Development

Run the test suite with:

```bash
cargo test
```

## License

MIT © ApocalypsAI
