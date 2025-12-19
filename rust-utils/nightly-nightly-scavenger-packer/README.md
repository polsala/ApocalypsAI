# Scavenger Packer

A whimsical Rust CLI that helps post‑apocalyptic scavengers pack the most valuable loot within a weight limit using the classic 0/1 knapsack algorithm.

## Features

- Read items from a CSV file (`name,weight,value`).
- Specify maximum carry weight.
- Outputs the optimal set of items and total value.

## Installation

```sh
cargo build --release
```

The binary will be at `target/release/scavenger-packer`.

## Usage

```sh
./scavenger-packer --items items.csv --capacity 15
```

Example `items.csv`:

```
mutated radroach,3,10
scrap metal,5,7
bottled water,2,5
old battery,4,8
```

Output:

```
Selected items:
- mutated radroach (weight: 3, value: 10)
- bottled water (weight: 2, value: 5)
- old battery (weight: 4, value: 8)
Total weight: 9
Total value: 23
```

## Testing

```sh
cargo test
```
