# Scavenger Knapsack

A whimsical CLI tool for post‑apocalypse survivors to choose the optimal set of items to carry, maximizing utility while staying within a weight limit. Uses the classic 0/1 knapsack algorithm.

## Usage

```sh
# Example: max weight 5
echo -e "water 3 10\nfood 2 8\nradio 1 5" | cargo run --release -- 5
```

The first argument is the maximum weight you can carry. Each line on stdin describes an item: `<name> <weight> <utility>`.

The program outputs the names of the selected items, one per line.

## Build & Test

```sh
cargo build --release
cargo test
```
