# nightly-waste-decay-simulator

A whimsical CLI tool that simulates radioactive waste decay using half‑life mathematics. Perfect for post‑apocalyptic role‑playing games or just for fun.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js <initial-grams> <half-life-days> <elapsed-days>
```

Example:

```sh
node src/index.js 1000 30 90
# => 125.00 grams remaining after 90 days
```

## API

```js
const { calculateRemaining } = require('./index');

/**
 * Calculates remaining amount after decay.
 * @param {number} initial - initial amount (grams)
 * @param {number} halfLife - half‑life period (days)
 * @param {number} days - elapsed time (days)
 * @returns {number} remaining amount (grams)
 */
```
