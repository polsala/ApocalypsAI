# nightly-rust-void-whisperer

A blazingly fast CLI utility written in Rust to encode and decode secret messages using a custom void cipher.

## Features

- Fast encoding/decoding of text using a custom algorithm
- CLI interface with subcommands
- Cross-platform support

## Usage

```bash
# Encode a message
void-whisperer encode "secret message"

# Decode a message
void-whisperer decode "encoded_output"
```

## Installation

```bash
cargo build --release
```

## Tests

Run tests with:

```bash
cargo test
```
