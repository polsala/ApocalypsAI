# Emoji Phrase Decoder

A tiny Rust CLI that translates a sequence of emojis into possible English phrases using a built‑in dictionary. Emojis are supplied separated by spaces.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
emoji-phrase-decoder 🌞 🍎
# => sun apple
```

Multiple meanings:

```sh
emoji-phrase-decoder 🐱
# => cat
# => kitten
```

## How it works

The tool contains a static map from emojis to one or more words. It computes the Cartesian product of the word lists for the supplied emojis and prints each combination on its own line.
