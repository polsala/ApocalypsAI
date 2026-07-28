# nightly-scavenger-packer

Utility to help post‑apocalyptic scavengers decide which loot to carry given a weight limit. Implements a classic 0/1 knapsack algorithm.

## Installation

```sh
npm install -g nightly-scavenger-packer
```

## Usage

```js
const { packItems } = require('./src/packer');

const items = [
  { name: 'Canned Beans', weight: 2, value: 3 },
  { name: 'Water Bottle', weight: 3, value: 4 },
  { name: 'First Aid Kit', weight: 5, value: 8 },
];

const capacity = 5;
const packed = packItems(items, capacity);
console.log(packed); // e.g., ['Canned Beans', 'Water Bottle']
```

## API

`packItems(items, capacity)` – returns an array of item names that maximize total value without exceeding the given capacity.
