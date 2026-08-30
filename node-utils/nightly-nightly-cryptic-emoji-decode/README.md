# nightly-cryptic-emoji-decoder

A whimsical Node.js CLI utility that encodes plain text into a sequence of emojis and decodes emoji sequences back to text. Great for secret messages, puzzles, or just adding a splash of fun to your chats.

## Installation

```sh
git clone <repo-url>
cd utils/nightly-cryptic-emoji-decoder
npm install
```

*(No external dependencies required.)*

## Usage

```sh
node src/index.js encode "HELLO"
# => 🐸🐸🐶🐶🐱

node src/index.js decode "🐸🐸🐶🐶🐱"
# => HELLO
```

## How it works

The utility maps the 26 English letters (A‑Z) to a fixed list of 26 animal emojis. Encoding converts each letter to its corresponding emoji; decoding does the reverse, substituting unknown emojis with `?`.

## Testing

```sh
node tests/test_index.js
```
