# nightly-emoji-mood-analyzer

A tiny Node.js commandâline utility that reads a line of text from standard input and prints a single emoji that reflects the overall mood of the message.

## How it works

The tool uses a handcrafted list of positive and negative words. It counts how many of each appear in the input (caseâinsensitive). If the positive count is greater than the negative count, it prints a happy emoji (ð). If the negative count is greater, it prints a sad emoji (ð¢). If the counts are equal or no sentiment words are found, it prints a neutral emoji (ð).

## Installation

```bash
# Clone the repository (or copy the utility folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-mood-analyzer
# Install Node.js if you haven't already
# No external dependencies are required
```

## Usage

```bash
# Pipe a sentence into the CLI
echo "I love sunny days but hate traffic" | node src/main.js
# Output: ð (more positive words)

# Directly run and type input (press Ctrl+D to end)
node src/main.js
I am feeling terrible today.
# Output: ð¢
```

## Testing

Run the test suite with Node's builtâin `assert` module:

```bash
npm test
```

The tests are located in `tests/test_main.js` and cover several sentiment scenarios.

## License

MIT â see the LICENSE file in the repository root.

