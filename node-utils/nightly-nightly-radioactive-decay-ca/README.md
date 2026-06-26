# Nightly Radioactive Decay Calculator

A whimsical yet practical Node.js CLI that calculates how much of a radioactive substance remains after a given elapsed time, based on its half‑life.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/cli.js <initial-amount> <half-life> <elapsed-time>
```

- `initial-amount` – starting quantity (any unit)
- `half-life` – half‑life of the isotope (same time unit as elapsed)
- `elapsed-time` – time that has passed

The program prints the remaining amount.

## Example

```sh
node src/cli.js 100 30 90
```

Outputs:

```
Remaining amount: 12.5
```

## API

```js
const { calculateRemaining } = require('./decay');
const remaining = calculateRemaining(100, 30, 90); // 12.5
```

## License

MIT
