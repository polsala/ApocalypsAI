# Nightly Emoji Crypt

**nightly-emoji-crypt** is a tiny Rust command‑line tool that translates plain text into a playful emoji cipher and can reverse the process.

## Features
- Encode any ASCII text (letters and spaces) into a deterministic emoji sequence.
- Decode an emoji sequence back to the original text.
- Zero‑runtime dependencies – just the Rust standard library.

## Installation
```bash
# Clone the repository (or copy the generated folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd rust-utils/nightly-emoji-crypt

# Build the binary
cargo build --release

# The executable will be at target/release/emoji-crypt
```

## Usage
```bash
# Encode a phrase
./target/release/emoji-crypt encode "hello world"
# => 😄😉😗😗⬜😙😗😍😗😎

# Decode the emoji string back to text
./target/release/emoji-crypt decode "😄😉😗😗⬜😙😗😍😗😎"
# => hello world
```

## Emoji Mapping
| Char | Emoji |
|------|-------|
| a | 😀 |
| b | 😁 |
| c | 😂 |
| d | 😃 |
| e | 😄 |
| f | 😅 |
| g | 😆 |
| h | 😉 |
| i | 😊 |
| j | 😋 |
| k | 😎 |
| l | 😍 |
| m | 😘 |
| n | 🥰 |
| o | 😗 |
| p | 😙 |
| q | 😚 |
| r | 🙂 |
| s | 🤗 |
| t | 🤩 |
| u | 🤔 |
| v | 🤨 |
| w | 😐 |
| x | 😑 |
| y | 😶 |
| z | 🙄 |
| (space) | ⬜ |

Any character not listed (digits, punctuation, etc.) is passed through unchanged.

## Testing
```bash
cargo test
```
All tests are deterministic and run offline.
