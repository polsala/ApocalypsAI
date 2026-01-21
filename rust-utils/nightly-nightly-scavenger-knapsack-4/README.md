# Scavenger Knapsack Optimizer

Utility to select the most valuable items to carry in a post‑apocalypse scavenging run given a weight limit. Input and output are JSON.

## Usage

```sh
cat payload.json | cargo run --quiet
```

`payload.json` format:

```json
{
  "capacity": 10,
  "items": [
    {"name": "canned beans", "weight": 3, "value": 5},
    {"name": "water bottle", "weight": 2, "value": 4},
    {"name": "first aid kit", "weight": 5, "value": 10}
  ]
}
```

Output:

```json
["canned beans","first aid kit"]
```

## Building

```sh
cargo build --release
```

## Testing

```sh
cargo test
```
