# nightly-scavenger-knapsack

A whimsical yet practical command‑line utility for the post‑apocalypse scavenger who needs to pack the most valuable loot without exceeding a weight limit.

## Features

- Reads a simple text format from **STDIN**:
  - First line: maximum weight the scavenger can carry (integer).
  - Subsequent lines: `name weight value` (space‑separated). Example:
    ```
    10
    water 5 10
    food 4 7
    medkit 6 12
    ```
- Computes the optimal subset of items using the classic 0/1 knapsack algorithm.
- Outputs the selected item names, one per line, in the order they appear in the input.

## Installation

```bash
# Ensure you have Rust toolchain installed (rustc and cargo)
cargo install --path .
```

## Usage

```bash
cat items.txt | scavenger-knapsack
```

Where `items.txt` follows the format described above.

## Example

```bash
$ cat <<EOF | scavenger-knapsack
10
water 5 10
food 4 7
medkit 6 12
EOF
water
food
```

The tool selected *water* and *food* (total weight 9, total value 17), which is the optimal combination under the weight limit of 10.

## Testing

Run the test suite with:

```bash
cargo test
```

---

*Enjoy your scavenging!*
