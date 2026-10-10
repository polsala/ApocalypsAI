# nightly-gear-weight-calculator

Utility to sum up gear weights for post‑apocalyptic survivors. Accepts a JSON file describing items with weight and unit (kg or lb) and outputs the total weight in both kilograms and pounds.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js path/to/items.json
# or pipe JSON via stdin
cat items.json | node src/index.js
```

## Input format

```json
[
  {"name":"Backpack","weight":5,"unit":"kg"},
  {"name":"Water Bottle","weight":2,"unit":"lb"}
]
```

## Output

```json
{"totalKg":5.907184,"totalLb":13.0231}
```

## Testing

```sh
npm test
```
