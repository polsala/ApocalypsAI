# Nightly Emoji Binary Encoder

## Overview

`nightly-emoji-binary-encoder` is a tiny Rust CLI tool that turns a non‑negative integer into a visual binary string made of emojis:

- `0` → ⚫ (black circle)
- `1` → 🔴 (red circle)

It’s perfect for adding a splash of post‑apocalyptic flair to your messages, logs, or secret codes.

## Installation

```bash
# Clone the repository (or copy the generated folder) and build
cargo build --release
```

The binary will be located at `target/release/nightly-emoji-binary-encoder`.

## Usage

```bash
nightly-emoji-binary-encoder <non‑negative integer>
```

### Examples

```bash
$ nightly-emoji-binary-encoder 5
🔴⚫🔴
# 5 in binary is 101 → 🔴⚫🔴

$ nightly-emoji-binary-encoder 13
🔴⚫🔴🔴
# 13 in binary is 1101 → 🔴⚫🔴🔴
```

If the input is not a valid integer, the program prints an error message and exits with a non‑zero status.

## Testing

Run the test suite with:

```bash
cargo test
```

All tests are deterministic and run offline.
