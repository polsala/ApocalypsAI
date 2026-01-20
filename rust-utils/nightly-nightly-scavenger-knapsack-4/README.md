# nightly-scavenger-knapsack

A whimsical CLI tool to help post‑apocalypse scavengers pack the most valuable loot within a limited carrying capacity. Implements the classic 0/1 knapsack algorithm.

## Usage

```sh
cat items.txt | cargo run --release -- <capacity>
```

`items.txt` format (one item per line):

```
<name> <weight> <value>
```

Example:

```
water 3 10
canned-food 2 7
first-aid 5 12
radio 1 4
```

Running with capacity 5:

```sh
cat items.txt | cargo run -- 5
```

Outputs the selected item names:

```
canned-food
radio
```

## Building

```sh
cargo build --release
```

## Testing

```sh
cargo test
```
