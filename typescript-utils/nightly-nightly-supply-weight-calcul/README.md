# nightly-supply-weight-calculator

Utility to compute the total weight of a list of supplies that may use mixed weight units. Provides a type‑safe TypeScript API and a convenient command‑line interface.

## Installation

```sh
npm install -g nightly-supply-weight-calculator
```

## Usage (CLI)

```sh
# Pipe a JSON array of supplies into the tool
cat supplies.json | npx nightly-supply-weight-calculator --unit kg
```

The JSON file should contain an array of objects with the following shape:

```json
[
  {"name":"Canned beans","weight":400,"unit":"g","quantity":3},
  {"name":"Water bottle","weight":1,"unit":"kg","quantity":2},
  {"name":"Rope","weight":2,"unit":"lb","quantity":1}
]
```

The `--unit` flag selects the output unit (`g`, `kg`, `lb`, or `oz`). If omitted, grams are used.

## API

```ts
import { computeTotalWeight, SupplyItem, WeightUnit } from "nightly-supply-weight-calculator";

const items: SupplyItem[] = [
  { name: "Canned beans", weight: 400, unit: "g", quantity: 3 },
  { name: "Water bottle", weight: 1, unit: "kg", quantity: 2 },
];

const totalKg = computeTotalWeight(items, "kg");
console.log(`Total weight: ${totalKg} kg`);
```

## Testing

Run the bundled tests with:

```sh
npm test
```

The test suite validates conversion accuracy and the CLI parsing logic.
