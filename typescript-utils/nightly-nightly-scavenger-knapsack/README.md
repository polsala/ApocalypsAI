# nightly-scavenger-knapsack

A whimsical TypeScript CLI utility for post‑apocalyptic scavengers. Given a list of potential loot items (name, weight, value) and a maximum carry weight, it computes the most valuable combination of items that fits within the weight limit (0/1 knapsack). Perfect for planning your next raid in the wasteland.

## Installation

```sh
npm install -g ts-node typescript
```

## Usage

Create a JSON file `loot.json`:

```json
[
  {"name":"Rusty Pipe","weight":5,"value":3},
  {"name":"Canned Beans","weight":2,"value":4},
  {"name":"Solar Battery","weight":7,"value":10}
]
```

Run:

```sh
ts-node src/index.ts loot.json 10
```

Output:

```
Selected items:
- Canned Beans (weight: 2, value: 4)
- Solar Battery (weight: 7, value: 10)
Total weight: 9
Total value: 14
```

## API

```ts
function computeKnapsack(items: Item[], maxWeight: number): Item[]
```

## Tests

Run the bundled test with:

```sh
ts-node tests/test_index.ts
```
