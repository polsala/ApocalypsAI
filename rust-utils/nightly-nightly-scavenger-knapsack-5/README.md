# nightly-scavenger-knapsack

A whimsical yet practical command‑line utility for the post‑apocalyptic survivor who needs to decide which scavenged items to carry.

## What it does

Given a weight limit (your backpack capacity) and a list of items (each with a name, weight, and value), the tool computes the optimal subset of items that maximizes total value without exceeding the weight limit – the classic 0/1 knapsack problem.

## Installation

```bash
# Ensure you have Rust and Cargo installed
cargo install --path .
```

## Usage

```bash
nightly-scavenger-knapsack <capacity> <items>
```

- `<capacity>` – maximum total weight you can carry (positive integer).
- `<items>` – comma‑separated list of items in the form `name:weight:value`.

### Example

```bash
nightly-scavenger-knapsack 5 water:3:10,food:2:7,medkit:5:12
```

Output:

```
Selected items:
 - water (weight: 3, value: 10)
 - food (weight: 2, value: 7)
Total value: 17
```

## How it works

The implementation uses a dynamic‑programming table to compute the maximum achievable value for every sub‑capacity and then back‑tracks to retrieve the chosen items.

## Testing

Run the test suite with:

```bash
cargo test
```

The tests cover the core knapsack solver with deterministic cases.
