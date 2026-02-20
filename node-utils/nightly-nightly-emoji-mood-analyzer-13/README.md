# nightly-emoji-mood-analyzer

A whimsical CLI utility that reads a line of text and returns an emoji representing the overall mood. It uses a tiny built‑in sentiment word list, so it works offline with zero dependencies.

## Installation

```sh
npm install -g .
```

(Assuming you place the utility in a folder and run `npm link`.)

## Usage

```sh
echo "I love sunny days!" | node src/index.js
# 😊

node src/index.js "I am feeling terrible today."
# 😢
```

## How it works

The script counts occurrences of a small set of positive and negative words. If positives > negatives → 😊, if negatives > positives → 😢, otherwise 😐.

## Testing

Run the bundled tests with:

```sh
node tests/test_index.js
```
