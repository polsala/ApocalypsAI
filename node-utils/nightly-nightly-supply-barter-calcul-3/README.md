# Nightly Supply Barter Calculator

Utility to compute fair trade values for post‑apocalyptic supplies based on scarcity.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/barter.js supplies.json
```

where `supplies.json` contains an array of items:

```json
[
  {"name":"canned beans","baseValue":10,"scarcity":0.8},
  {"name":"water bottle","baseValue":5,"scarcity":0.3}
]
```

The tool prints each item with its adjusted barter value, e.g.:

```json
[
  {"name":"canned beans","adjustedValue":11},
  {"name":"water bottle","adjustedValue":6.75}
]
```

## Algorithm

Adjusted value = `baseValue * (1 + (1 - scarcity) * 0.5)`

- `baseValue` – intrinsic worth of the item (numeric).
- `scarcity` – a number between `0` (abundant) and `1` (extremely scarce).
- The factor `0.5` gives a modest boost for rarer items while keeping values sane.

## Testing

Run the bundled tests with Node:

```sh
node tests/test_barter.js
```

All tests should pass, confirming deterministic behavior.
