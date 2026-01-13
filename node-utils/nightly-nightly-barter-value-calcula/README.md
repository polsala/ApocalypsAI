# Nightly Barter Value Calculator

A whimsical yet practical Node.js utility that estimates the barter value (in scrap) of common postâapocalyptic items.

## Features

- Small builtâin catalogue of items with base values.
- Condition multipliers (pristine, good, worn, broken).
- CLI interface: `node src/index.js <item> <condition>`
- Exported `calculateValue(item, condition)` function for programmatic use and testing.

## Installation

```bash
# Clone the repository (or copy the utility folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-barter-value-calculator
# No external dependencies required â just Node.js (v14+)
```

## Usage

```bash
node src/index.js water good
# => Barter value for "water" (good condition): 15 scrap

node src/index.js "firstâaid kit" pristine
# => Barter value for "firstâaid kit" (pristine): 45 scrap
```

## API

```js
const { calculateValue } = require('./src/index.js');

const value = calculateValue('ammo', 'worn');
console.log(value); // 8
```

## Testing

Run the bundled tests with Node:

```bash
node tests/test_index.js
```

All tests should pass without any external network calls.

---

*Created by the ApocalypsAI Nightly Integrator agent.*
