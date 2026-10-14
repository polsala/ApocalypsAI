# Nightly Radiation Decay Estimator

A tiny, whimsical Node.js utility that tells you how much of a radioactive isotope is left after a certain amount of time.

## Features

- Supports a handful of well‑known isotopes (U‑235, U‑238, C‑14, I‑131).
- Simple CLI interface (`--isotope` and `--years`).
- Exposes a programmatic function `estimateDecay(isotope, years)` for use in other scripts.

## Installation

```bash
# Clone the repository (or copy the utility folder) and install dependencies
npm install
```

> **Note**: This utility has **no external dependencies**; the `npm install` step is only for completeness.

## Usage

```bash
node src/main.js --isotope=U-235 --years=1000000
```

Output example:

```
Isotope: U-235
Years elapsed: 1000000
Remaining activity: 0.7079 (70.79% of original)
```

## Programmatic API

```js
const { estimateDecay } = require('../src/main');

const fraction = estimateDecay('C-14', 11460); // two half‑lives
console.log(fraction); // 0.25
```

## Testing

Run the bundled tests with:

```bash
node tests/test_main.js
```

All tests should pass and produce no output on success.
