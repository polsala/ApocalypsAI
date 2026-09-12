# Nightly Scavenger Knapsack

A whimsical command‑line utility for apocalyptic scavengers. Given a JSON list of items (name, weight, value) and a maximum carry weight, it computes the optimal set of items to maximize total value.

## Usage

```sh
cargo run --release -- <items.json> <max_weight>
```

`items.json` example:

```json
[
  {"name":"Canned Beans","weight":2,"value":5},
  {"name":"Water Bottle","weight":3,"value":4},
  {"name":"First Aid Kit","weight":5,"value":10}
]
```

Output: JSON array of selected item names.

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
