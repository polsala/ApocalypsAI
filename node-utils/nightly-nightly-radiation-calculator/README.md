# nightly-radiation-calculator

Estimates a safe distance from a radiation source based on the reported exposure level (in sieverts).  The tool is deliberately whimsical – perfect for a post‑apocalyptic community that still wants to stay safe while having a little fun.

## Installation

```sh
# Clone the repository (or copy the utility folder) and install globally
npm install -g .
```

> **Note**: The utility has no external dependencies beyond the Node.js standard library.

## Usage

```sh
node src/main.js <sieverts>
```

Replace `<sieverts>` with the measured radiation level (a positive number).  The program will print a safe distance in meters and a whimsical message.

### Example

```sh
$ node src/main.js 0.5
Safe distance: 2.00 meters. Stay safe, wanderer!
```

## How it works

The calculation is a simplified model based on the inverse‑square law:

```
 distance = sqrt( 1 / (sieverts * 0.5) )
```

The constant `0.5` is a fictional attenuation factor chosen for a balance between realism and playfulness.  The result is rounded to two decimal places.

## API

The core function can be required in other Node projects:

```js
const { calculateSafeDistance } = require('./src/main');
const distance = calculateSafeDistance(0.3);
console.log(distance); // => 2.58
```

## Testing

Run the test suite with:

```sh
node tests/test_main.js
```

All tests should pass without external network access.
