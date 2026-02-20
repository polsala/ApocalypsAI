# nightly-emoji-mood-analyzer

A tiny Node.js utility that reads a piece of text and returns an emoji representing its overall mood. Uses a simple word‑based sentiment scoring algorithm, no external dependencies.

## Installation

```sh
npm install
```

## Usage

```sh
node src/index.js "I love sunny days"
# 😊
```

Or use as a module:

```js
const { analyzeMood } = require('./src/index');
console.log(analyzeMood("I'm feeling terrible"));
```

## How it works

The script maintains small lists of positive and negative words. Each occurrence adds +1 or -1 to a score. The final score maps to an emoji:

- score > 2 → 😄
- score 1‑2 → 😊
- score 0 → 😐
- score -1‑-2 → 🙁
- score < -2 → 😞

## Tests

Run `node tests/test_index.js`.
