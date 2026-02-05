# nightly‑scavenger‑inventory

A tiny Rust CLI for the wandering scavenger.

## What it does

- Accept a **maximum carry weight** (float) as the first argument.
- Accept a list of items in the form `name:weight` (e.g. `water:2.5`).
- Compute the total weight of all items.
- If the total exceeds the limit, suggest a minimal set of items to drop (greedy drop of heaviest items) so the remaining weight fits.

## Installation

```bash
# Clone the repository (or copy the generated folder) and build
git clone <repo‑url>
cd nightly-scavenger-inventory
cargo build --release
```

The binary will be at `target/release/nightly-scavenger-inventory`.

## Usage

```bash
# Basic example – limit 10.0 units
./target/release/nightly-scavenger-inventory 10 water:2 food:3 toolkit:5 ammo:1
```

**Output**
```
Total weight: 11.0
Limit exceeded by 1.0
Suggested items to drop: toolkit (5.0)
```

If the total weight is within the limit, it simply prints the total.

## Testing

```bash
cargo test
```

All tests run offline and use deterministic mock data.
