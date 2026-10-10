# nightly-emoji-mood-analyzer

A tiny Node.js utility that reads a short piece of text and returns an emoji that reflects the overall mood.

## Features

- **Zero dependencies** – pure JavaScript, works with any recent Node version.
- **CLI & library** – use it from the command line or import the `analyzeMood` function in your own code.
- **Whimsical sentiment** – a simple word‑list based sentiment detector that maps to three emojis:
  - 😊 for positive text
  - 😢 for negative text
  - 😐 for neutral/unknown text

## Installation

```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-mood-analyzer
# No external packages required – just install Node if you haven't already
```

## Usage

### As a CLI

```bash
node src/index.js "I love sunny days"
# => 😊

node src/index.js "I hate rainy weather"
# => 😢
```

If you omit the argument, the script will read from STDIN:

```bash
echo "It is an okay day" | node src/index.js
# => 😐
```

### As a library

```javascript
const { analyzeMood } = require('./src/index');

console.log(analyzeMood('Life is wonderful'));
// 😊
```

## Testing

Run the bundled tests with Node:

```bash
node tests/test_index.js
```

All tests should pass without any external dependencies.
