# nightly-emoji-crypt

**nightly-emoji-crypt** is a whimsical yet handy Rust command‑line tool that translates a sequence of emojis into a plain‑text message using a fixed substitution cipher.

## How it works
Each supported emoji maps to a single lower‑case letter:

| Emoji | Letter |
|-------|--------|
| 🐱   | a |
| 🐶   | b |
| 🐭   | c |
| 🐹   | d |
| 🐰   | e |
| 🦊   | f |
| 🐻   | g |
| 🐼   | h |
| 🐨   | i |
| 🐯   | j |

Any emoji not in the table is ignored.

## Installation
```bash
# Clone the repository (or copy the generated folder) and build
cargo build --release
```

The binary will be located at `target/release/nightly-emoji-crypt`.

## Usage
You can pass the emoji string as a command‑line argument or pipe it via STDIN.

```bash
# Argument mode
./nightly-emoji-crypt "🐱🐶🐭"
# => abc

# Pipe mode
echo "🐱🐶🐭" | ./nightly-emoji-crypt
# => abc
```

## Testing
Run the test suite with:
```bash
cargo test
```
All tests are deterministic and run offline.
