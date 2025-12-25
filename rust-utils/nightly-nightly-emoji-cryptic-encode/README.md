# Nightly Emoji Cryptic Encoder

A tiny, self‑contained Rust command‑line tool that converts arbitrary text into a sequence of emojis and back again. It works by:

1. Encoding the input as standard Base64.
2. Replacing each Base64 character with a unique emoji from a fixed 64‑emoji table.
3. Using the special emoji `🟰` for the Base64 padding character `=`.

The reverse operation restores the original text.

## Build

```bash
# Ensure you have Rust and Cargo installed
cargo build --release
```

The binary will be placed at `target/release/nightly-emoji-cryptic-encoder`.

## Usage

```bash
# Encode a string
./target/release/nightly-emoji-cryptic-encoder encode "Hello, world!"

# Decode an emoji string
./target/release/nightly-emoji-cryptic-encoder decode "🤗😆😴🟰"
```

## Example

```bash
$ ./target/release/nightly-emoji-cryptic-encoder encode "Hi"
🤗😆😴🟰
$ ./target/release/nightly-emoji-cryptic-encoder decode "🤗😆😴🟰"
Hi
```

## Testing

Run the test suite with:

```bash
cargo test
```

All tests are deterministic and run offline.
