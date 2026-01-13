# nightly-emoji-mood-analyzer

## Summary

Analyzes a line of text and outputs a single emoji representing the detected mood (happy, sad, angry, surprised, neutral). Useful for quick sentiment tagging in chats, commit messages, or logs.

## Installation

```sh
node src/main.js < input.txt
```

The utility has no external dependencies and runs with Node.js (v12+).

## Usage

```sh
echo "I am thrilled about the new release!" | node src/main.js
# => ð
```

Or pipe a file:

```sh
node src/main.js < messages.txt
```

## How it works

The script uses a tiny builtâin lexicon of positive and negative words. It counts matches and selects an emoji accordingly.

## Testing

```sh
node tests/test_main.js
```

If all assertions pass you will see `All tests passed`.

