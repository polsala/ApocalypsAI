# nightly-emoji-sentiment-cli

A whimsical CLI tool that estimates the sentiment of a piece of text based on the emojis it contains. Each emoji contributes a positive or negative weight; the total score indicates overall mood.

## Installation

```sh
npm install -g .
# or run directly with node
```

## Usage

```sh
echo "I love this! 😄👍" | node src/index.js
# => Sentiment score: 2
```

You can also pass the text as arguments:

```sh
node src/index.js "Feeling sad 😢"
# => Sentiment score: -1
```

## How it works

The tool contains a built‑in map of common emojis to sentiment values (+1 for happy, -1 for sad, etc.). It scans the input text, sums the values, and prints the total.

## Testing

```sh
npm test
```
