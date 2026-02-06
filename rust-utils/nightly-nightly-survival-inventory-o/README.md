# nightly‑survival‑inventory‑optimizer

A tiny Rust command‑line utility that helps you decide which items to pack in your survival kit.

## What it does

Given a list of items (each with a name, weight, and utility score) and a maximum carry weight, the tool computes the optimal subset of items that maximizes total utility while staying within the weight limit – classic 0/1 knapsack.

## Build & Run

```bash
# Build the binary (requires Rust toolchain)
cargo build --release

# Example usage
./target/release/nightly-survival-inventory-optimizer \
    --items "water:3:10,food:5:8,first‑aid:2:7,radio:1:4,knife:2:5" \
    --capacity 10
```

The above command will output something like:
```
Optimal items (total weight: 10, total utility: 27):
- water (3kg, utility 10)
- first‑aid (2kg, utility 7)
- radio (1kg, utility 4)
- knife (2kg, utility 5)
- food (5kg, utility 8)  <-- omitted because of weight limit
```

## Arguments

- `--items` – Comma‑separated list of items in the form `name:weight:utility`.
- `--capacity` – Maximum total weight you can carry (integer).

## Testing

Run the test suite with:
```bash
cargo test
```

All tests are deterministic and run offline.
