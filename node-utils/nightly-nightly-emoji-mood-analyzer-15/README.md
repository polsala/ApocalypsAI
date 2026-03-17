# nightly-emoji-mood-analyzer

A tiny, whimsical utility that reads a piece of text and returns an emoji that best represents the overall mood of the sentence.

## Features

- **Zero dependencies** – pure JavaScript, runs on any Node.js 14+ runtime.
- **Simple sentiment logic** – uses a small built‑in word list for positive and negative cues.
- **CLI friendly** – can be invoked directly from the command line.

## Installation

```bash
# Clone the repository (or copy the utility folder) and install (optional)
npm install
```

> No external packages are required; `npm install` will only create a `node_modules` folder for the test runner.

## Usage

```bash
node src/index.js "I love sunny days and fresh coffee!"
# => 😊

node src/index.js "I am frustrated with endless bugs."
# => 😠
```

If you omit the argument, the script will prompt you to provide a sentence.

## API

```js
const { analyzeMood } = require('./src/index.js');

const mood = analyzeMood('Your text here');
console.log(mood); // 😐, 😊, 😢, or 😠
```

## Testing

Run the bundled tests with:

```bash
npm test
```

The test suite uses Node's built‑in `assert` module and does not require any network access.

## License

MIT © ApocalypsAI Community
