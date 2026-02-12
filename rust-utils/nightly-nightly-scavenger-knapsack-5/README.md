# nightly-scavenger-knapsack

A whimsical command‑line tool that helps post‑apocalypse scavengers pick the most valuable items to carry without exceeding their weight limit. Implements a simple greedy knapsack algorithm.

## Usage

```sh
cargo run --release -- <items.json> <max_weight>
```

`items.json` format:

```json
[
  {"name":"Canned Beans","weight":2,"value":5},
  {"name":"Water Bottle","weight":3,"value":4},
  {"name":"First Aid Kit","weight":5,"value":10}
]
```

The program prints the selected item names and total value.

## Example

```sh
$ cargo run -- items.json 7
Selected items: ["First Aid Kit","Canned Beans"]
Total value: 15
```

## Testing

```sh
cargo test
```
