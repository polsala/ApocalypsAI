# nightly-emoji-mood-analyzer

A tiny Node.js command‑line utility that takes a piece of text and returns an emoji that reflects the overall mood of the sentence.

## Features

- **Zero external dependencies** – pure JavaScript, runs on any Node 14+.
- **Simple sentiment engine** – uses a small built‑in word list for positive and negative words.
- **Whimsical output** – happy 😄, neutral 😐, or sad 😞 emojis.
- **Cross‑platform** – works on Windows, macOS, and Linux.

## Installation

```bash
npm install -g nightly-emoji-mood-analyzer
```

*(The package is not published to npm; you can link it locally after cloning the repository:)*

```bash
npm link
```

## Usage

```bash
emoji-mood "I love sunny days and fresh coffee!"
# => 😄

emoji-mood "It is an ordinary day."
# => 😐

emoji-mood "I am frustrated with endless bugs."
# => 😞
```

You can also pipe input:

```bash
echo "I feel great" | emoji-mood
```

## How it works

The script tokenises the input, counts how many words appear in a tiny positive and negative word list, and computes a simple score:

- **score > 1** → happy 😄
- **score < -1** → sad 😞
- otherwise → neutral 😐

## Development

```bash
# Install dependencies (none needed) and run tests
npm test
```

## License

MIT © ApocalypsAI
