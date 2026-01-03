# nightly-emoji-roulette

A whimsical command‑line tool that takes a sentence and wraps each word with an emoji. The emoji is chosen deterministically based on the first letter of the word, so the output is reproducible.

## Features

- **Deterministic emoji selection** – no random state, making the output predictable.
- **Simple and fast** – written in Rust, no external dependencies.
- **Works with stdin or command‑line arguments**.

## Installation

```bash
# Using Cargo
cargo install nightly-emoji-roulette
```

## Usage

```bash
# From a string argument
nightly-emoji-roulette "Hello world"
# Output: 🤣Hello🤣 😄world😄

# From stdin
echo "Rust is fun" | nightly-emoji-roulette
# Output: 🤣Rust🤣 😄is😄 🤣fun🤣
```

## How It Works

The utility maps the first letter of each word to an emoji from a fixed list:

```text
Index: 0  1  2  3  4  5  6  7  8  9
Emoji: 😀 😃 😄 😁 😆 😅 😂 🤣 😊 😇
```

The mapping is calculated as `(first_letter_ascii - 'a') % 10`. Non‑alphabetic words default to the first emoji.

## License

MIT
