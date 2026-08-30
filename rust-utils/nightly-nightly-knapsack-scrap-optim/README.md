# Nightly Knapsack Scrap Optimizer

A tiny Rust CLI that helps post‑apocalypse scavengers pick the most valuable set of items without exceeding a weight limit. It uses the classic 0/1 knapsack dynamic programming algorithm.

## Usage

```sh
cargo run --release -- <items.json> <max_weight>
```

`items.json` format:

```json
[
  {"name":"Rusty Pipe","weight":4,"value":3},
  {"name":"Canned Food","weight":2,"value":6},
  {"name":"Battery Pack","weight":3,"value":5}
]
```

The program prints the selected item names and the total value.

## Example

```sh
$ cargo run --release -- items.json 5
Selected items: ["Canned Food","Battery Pack"]
Total value: 11
```

## Testing

```sh
cargo test
```
