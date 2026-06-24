# nightly-backpack-optimizer

A whimsical yet practical Node.js CLI that helps post‑apocalyptic survivors pack their backpacks. Given a list of items (name, weight, utility value) and a maximum weight capacity, it selects the combination of items that maximizes total utility using the classic 0/1 knapsack algorithm.

## Install

```sh
npm install -g .
```

(Assuming you copy the folder and run `npm install -g`.)

## Usage

```sh
node src/index.js --limit 10 --items '[{"name":"water","weight":3,"value":5},{"name":"food","weight":4,"value":6},{"name":"radio","weight":2,"value":2}]'
```

Output (JSON array of selected items):

```json
[{"name":"water","weight":3,"value":5},{"name":"food","weight":4,"value":6}]
```

## API

```js
const { solveKnapsack } = require('./index');
const items = [{name:'water', weight:3, value:5}, {name:'food', weight:4, value:6}, {name:'radio', weight:2, value:2}];
const best = solveKnapsack(items, 10);
```

## Tests

Run `npm test` (uses Node's built‑in assert).
