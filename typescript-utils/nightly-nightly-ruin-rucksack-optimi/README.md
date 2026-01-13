# nightly-ruin-rucksack-optimizer

A whimsical TypeScript commandâline utility that helps postâapocalyptic scavengers pack the most valuable loot without exceeding their carrying capacity. It solves the classic 0/1 knapsack problem.

## Features

* Typeâsafe TypeScript implementation
* Simple CLI: `node dist/main.js --items items.json --capacity 50`
* Returns the optimal subset of items as JSON

## Installation

```sh
npm install
npm run build
```

## Usage

Create an `items.json` file:

```json
[
  { "name": "Canned Beans", "weight": 2, "value": 3 },
  { "name": "Water Bottle", "weight": 3, "value": 4 },
  { "name": "First Aid Kit", "weight": 5, "value": 10 }
]
```

Run the optimizer:

```sh
node dist/main.js --items items.json --capacity 5
```

Output:

```json
[
  { "name": "First Aid Kit", "weight": 5, "value": 10 }
]
```

## Testing

```sh
npm test
```

## License

MIT
