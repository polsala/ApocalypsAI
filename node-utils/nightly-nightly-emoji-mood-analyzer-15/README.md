# nightly-emoji-mood-analyzer

A whimsical CLI utility that reads a line of text and outputs an emoji reflecting its mood.

## Installation

```sh
npm install -g .
```

## Usage

```sh
echo "I love sunny days!" | node src/main.js
# 😊
```

Or as a module:

```js
const { analyzeMood } = require('./src/main');
console.log(analyzeMood("I'm feeling terrible."));
// 😢
```

## How it works

Simple word‑list based sentiment detection. The tool counts occurrences of a small set of positive and negative words and chooses an emoji:

- More positive words → 😊
- More negative words → 😢
- Equal or none → 😐
