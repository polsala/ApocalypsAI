# nightly-emoji-mood-analyzer

A tiny Node.js utility that reads a short piece of text and returns an emoji that best matches the mood. Perfect for adding a splash of personality to logs, chat bots, or commit messages.

## Installation

```sh
npm install -g nightly-emoji-mood-analyzer
```

*(In this repository you can run it directly with Node.)*

## Usage

```sh
node src/main.js "I am feeling great!"
# => 😊
```

If no argument is provided, the utility reads from STDIN:

```sh
echo "I'm sad." | node src/main.js
# => 😢
```

## API

```js
const { analyzeMood } = require('./main');
console.log(analyzeMood("I love this!")); // ❤️
```

## Supported moods

- happy 😊
- sad 😢
- angry 😠
- love ❤️
- fear 😨
- surprise 😲
- neutral 🤔 (default)
