# Scavenger Packer

A whimsical CLI utility for post‑apocalypse scavengers to maximize loot value within a weight limit using the classic 0/1 knapsack algorithm.

## Installation

```sh
cargo build --release
```

The binary will be located at `target/release/scavenger-packer`.

## Usage

```sh
./target/release/scavenger-packer <capacity> <item1> <item2> ...
```

Each item is specified as `name:weight:value`. Example:

```sh
./target/release/scavenger-packer 15 "canned-food:3:10" "water:5:8" "medkit:4:12" "radio:2:5"
```

The program prints the selected items and the total value.

## How It Works

The tool implements a dynamic‑programming solution to the 0/1 knapsack problem, guaranteeing the optimal selection of items for the given capacity.
