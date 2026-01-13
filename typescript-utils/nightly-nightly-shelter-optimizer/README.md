# nightly-shelter-optimizer

A whimsical yet practical TypeScript command‑line utility for post‑apocalyptic survivors.
It solves a classic 0/1 knapsack problem: given a list of supplies (each with a weight and a value) and a shelter weight limit, it picks the combination of items that yields the highest total value without exceeding the limit.

## Features

- Pure TypeScript, no external runtime dependencies beyond Node.js.
- Reads input from a JSON file or STDIN.
- Outputs the chosen items, total weight, and total value in a human‑readable format.
- Includes a deterministic test suite that can be run with `npm test`.

## Installation

```bash
# Clone the repository (or let the ApocalypsAI agent add this utility)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-shelter-optimizer

# Install dependencies
npm install
```

## Usage

```bash
# Using a JSON file
node dist/main.js -i supplies.json

# Piping JSON via STDIN
cat supplies.json | node dist/main.js
```

The input JSON must have the following shape:

```json
{
  "capacity": 50,
  "items": [
    {"name": "Canned Beans", "weight": 5, "value": 10},
    {"name": "Water Bottle", "weight": 10, "value": 15},
    {"name": "First‑Aid Kit", "weight": 8, "value": 25}
  ]
}
```

### Example Output

````
Selected items:
- Canned Beans (weight: 5, value: 10)
- First‑Aid Kit (weight: 8, value: 25)

Total weight: 13
Total value: 35
````

## Testing

```bash
npm test
```

The test suite validates the knapsack algorithm against a known scenario.

## License

MIT – see LICENSE file in the repository root.

