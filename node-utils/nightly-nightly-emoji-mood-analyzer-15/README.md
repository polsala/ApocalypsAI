# nightly-emoji-mood-analyzer

A whimsical utility that reads a line of text and returns an emoji representing the overall mood. Useful for adding emotional flair to logs, commit messages, or chat bots.

## Installation

```sh
npm install
node src/index.js "I am feeling great today!"
```

## Usage

```js
const { analyzeMood } = require('./src/index');
console.log(analyzeMood("I'm so sad.")); // 😢
```

## CLI

```sh
node src/index.js "Your text here"
```

## How it works

Simple keyword matching against a small dictionary of mood words.
