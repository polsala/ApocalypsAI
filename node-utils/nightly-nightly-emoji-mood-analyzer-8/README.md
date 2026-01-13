# nightly-emoji-mood-analyzer

A whimsical CLI utility that reads a piece of text and returns an emoji representing the overall mood. Uses simple keyword matching to guess happiness, sadness, anger, fear, or surprise.

## Installation

```sh
npm install -g .
```

## Usage

```sh
echo "I am thrilled!" | nemoji
# or
nemoji "I am thrilled!"
```

Outputs an emoji like ð.

## How it works

The tool scans the input for keywords associated with five moods and returns the corresponding emoji. If no keywords are found, it returns ð¤.

## License

MIT
