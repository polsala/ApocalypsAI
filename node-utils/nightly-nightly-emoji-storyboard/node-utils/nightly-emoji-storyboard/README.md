# nightly-emoji-storyboard

**nightly-emoji-storyboard** is a tiny Node.js CLI utility that turns any sentence into a space‑separated sequence of emojis – one emoji per word.  It’s perfect for adding a splash of visual flair to chat messages, notes, or social‑media posts.

---

## Installation

```bash
# Clone the repository (or copy the utility folder) and install dependencies (none required beyond Node.js)
# Ensure you have Node.js v14+ installed
```

The utility is self‑contained; no external packages are needed.

---

## Usage

```bash
node src/index.js "Your sentence here"
```

**Example**

```bash
$ node src/index.js "I love cats and dogs while drinking coffee"
❓ ❤️ 🐱 ❓ 🐶 ❓ ☕
```

The tool maps known words to emojis (see source for the built‑in dictionary). Unknown words are represented by the ❓ emoji.

---

## API

The core function can be required in other Node projects:

```js
const { generateStoryboard } = require('./src/index');

const emojis = generateStoryboard('happy sun rain');
console.log(emojis); // 😊 ☀️ 🌧️
```

---

## Testing

Run the bundled tests with Node:

```bash
node tests/test_index.js
```

All tests should pass, confirming deterministic behavior.

---

## License

MIT © ApocalypsAI Community
