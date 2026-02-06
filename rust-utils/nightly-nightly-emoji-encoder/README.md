# nightly-emoji-encoder

Encode plain text into a string of regional indicator emoji flags representing each alphabetic character. Non‑alphabetic characters are left unchanged.

## Usage

```sh
cargo run -- "Hello, World!"
# Output: 🇭🇪🇱🇱🇴, 🇼🇴🇷🇱🇩!
```

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
