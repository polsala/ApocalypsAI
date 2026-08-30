# nightly-emoji-crypt

`nightly-emoji-crypt` is a tiny command‑line utility written in Rust that translates ordinary ASCII text into a string of emojis and back again.  It’s perfect for leaving hidden notes in chat, adding a splash of fun to logs, or just playing secret‑message games.

## Installation

```bash
# Clone the repository (or copy the generated folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-emoji-crypt

# Build the binary with Cargo
cargo build --release
```

The compiled binary will be located at `target/release/nightly-emoji-crypt`.

## Usage

```bash
# Encode a phrase
./target/release/nightly-emoji-crypt encode "hello world"
# => 🦊🐘🦁🦁🦒 🌞🦁🦒🦁🦊

# Decode the emoji string back to text
./target/release/nightly-emoji-crypt decode "🦊🐘🦁🦁🦒 🌞🦁🦒🦁🦊"
# => hello world
```

The tool supports lower‑case letters `a‑z`, digits `0‑9`, and spaces.  Any unsupported character is passed through unchanged.

## Testing

Run the test suite with:

```bash
cargo test
```

All tests are deterministic and run offline.

## License

MIT © ApocalypsAI community
