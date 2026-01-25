# Nightly Scavenger Knapsack

A whimsical command‑line utility that helps you pick the most valuable items to carry in a post‑apocalypse scavenger run, given a weight limit. It solves the classic 0/1 knapsack problem.

## Build

```sh
cargo build --release
```

## Usage

```sh
nightly-scavenger-knapsack --capacity <MAX_WEIGHT> --items <CSV_FILE>
```

The CSV file should have no header and each line formatted as:

```
name,weight,value
```

Example:

```
water,3,10
food,2,9
radio,1,4
```

The program prints the selected item names, comma‑separated.

## Tests

```sh
cargo test
```
