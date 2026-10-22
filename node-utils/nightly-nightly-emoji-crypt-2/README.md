# nightly-emoji-crypt

**nightly-emoji-crypt** is a tiny Node.js command‑line utility that lets you *encode* plain text into a string of emojis and *decode* it back again.  It uses a fixed, reversible substitution table so the transformation is deterministic and completely offline.

## Features

- Encode any ASCII text (letters, digits, space) into a fun emoji string.
- Decode an emoji string back to the original text.
- Unknown characters are passed through unchanged, making the tool tolerant of punctuation.
- Zero external dependencies – just plain Node.js.

## Installation

```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-crypt
npm install   # only installs dev dependencies for testing (none required for runtime)
```

## Usage

```bash
# Encode a message
node src/index.js encode "Hello World 123"
# => 🦁🦊🐵🐵🦁 🌞🦁🐵🦊🦁 1️⃣2️⃣3️⃣

# Decode a message
node src/index.js decode "🦁🦊🐵🐵🦁 🌞🦁🐵🦊🦁 1️⃣2️⃣3️⃣"
# => Hello World 123
```

The first argument is the **action** (`encode` or `decode`).  All remaining arguments are joined with spaces to form the input string.

## Development & Testing

Run the bundled tests with:

```bash
node tests/test_index.js
```

All tests should pass without any network access.

## License

MIT © ApocalypsAI community
