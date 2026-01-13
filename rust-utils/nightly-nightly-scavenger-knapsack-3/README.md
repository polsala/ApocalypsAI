# Scavenger Knapsack

A whimsical CLI tool to help postâapocalypse scavengers decide which items to carry given a weight limit. Implements the classic 0/1 knapsack algorithm.

## Usage

```sh
cargo run --release -- <capacity> <item1_weight>:<item1_value> <item2_weight>:<item2_value> ...
```

Example:

```sh
cargo run -- 15 3:4 4:5 7:10 8:11 9:13
```

Outputs the maximum total value achievable.

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
