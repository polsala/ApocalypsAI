# nightly-emoji-mood-analyzer

A tiny Node.js utility that reads a short piece of text and returns an emoji representing the overall mood.

## Features

- **Whimsical**: Turns feelings into emojis.
- **Zero dependencies**: Pure JavaScript, no external packages.
- **CLI friendly**: Use it directly from the command line.

## Installation

```bash
# Clone the repository (or copy the utility folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-mood-analyzer
# No npm install needed â the script has no external deps
```

## Usage

```bash
node src/main.js "I love sunny days and fresh coffee!"
# => ð

node src/main.js "I am feeling okay, nothing special."
# => ð

node src/main.js "Everything is falling apart..."
# => ð¢
```

If you want to use the function programmatically:

```js
const { analyzeMood } = require('./src/main.js');
console.log(analyzeMood('I am thrilled!')); // ð
```

## How it works

The script contains two small word lists â one for positive words and one for negative words. It scores the input text by adding +1 for each positive word and -1 for each negative word. The final score determines the emoji:

- **score > 0** â ð (happy)
- **score == 0** â ð (neutral)
- **score < 0** â ð¢ (sad)

## Testing

Run the bundled tests with Node:

```bash
node tests/test_main.js
```
All tests should pass without any external network calls.

