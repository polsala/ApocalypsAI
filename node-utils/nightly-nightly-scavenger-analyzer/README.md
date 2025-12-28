# nightly-scavenger-analyzer

Utility to analyze a list of scavenged items from the post‑apocalypse. It reports total item count, total weight, and a breakdown of rarities.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js path/to/items.json
```

The JSON file should be an array of objects:

```json
[
  {"name":"Rusty Spoon","weight":0.2,"rarity":"common"},
  {"name":"Ancient Relic","weight":2.5,"rarity":"epic"}
]
```

The tool prints a summary JSON to stdout.

## Example

```sh
$ node src/index.js sample.json
{
  "totalItems": 2,
  "totalWeight": 2.7,
  "rarityCounts": {"common":1,"epic":1}
}
```
