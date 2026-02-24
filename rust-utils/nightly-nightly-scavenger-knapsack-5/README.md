# nightly‑scavenger‑knapsack

**A whimsical yet practical Rust CLI** that helps a post‑apocalypse scavenger pick the most valuable items they can carry without exceeding a weight limit.

## What it does
- Reads a JSON file describing items (name, weight, value).
- Takes a maximum carry weight (capacity) as a command‑line argument.
- Solves the classic 0/1 knapsack problem using dynamic programming.
- Prints the optimal set of items and the total value.

## Installation
```bash
# Clone the repository (or copy the generated folder) and build
cargo build --release
```

## Usage
```bash
# <input.json> is an array of objects: [{"name":"canned beans","weight":2,"value":5}, ...]
# <capacity> is the maximum total weight you can carry (integer)
cargo run --release -- <input.json> <capacity>
```

### Example
```json
[
  {"name": "canned beans", "weight": 2, "value": 5},
  {"name": "water bottle", "weight": 3, "value": 4},
  {"name": "first‑aid kit", "weight": 5, "value": 10},
  {"name": "flashlight", "weight": 1, "value": 2}
]
```
```bash
cargo run --release -- items.json 5
```
**Output**
```
Selected items:
- canned beans (weight: 2, value: 5)
- flashlight (weight: 1, value: 2)
Total weight: 3
Total value: 7
```

## Testing
```bash
cargo test
```
All tests are deterministic and run offline.

## License
MIT © ApocalypsAI
