# nightly-rot13-cli

A whimsical yet handy Rust command‑line utility that applies the classic ROT13 cipher to any input string.

## What is ROT13?
ROT13 is a simple letter substitution cipher that rotates each alphabetical character by 13 places. Because the Latin alphabet has 26 letters, applying ROT13 twice returns the original text. It’s often used for obscuring spoilers or secret messages.

## Why a CLI?
In a post‑apocalyptic world, you might need to quickly encode a note before passing it to a fellow scavenger. This tiny tool does exactly that – no dependencies, just a single binary.

## Installation
```bash
# Clone the repository (or copy the generated folder into your workspace)
git clone https://github.com/polsala/ApocalypsAI.git
cd rust-utils/nightly-rot13-cli

# Build the binary using Cargo (Rust's package manager)
cargo build --release
```
The compiled binary will be located at `target/release/nightly-rot13-cli`.

## Usage
```bash
# Encode a message
./target/release/nightly-rot13-cli "Hello, survivor!"
# => "Uryyb, fhesvire!"

# Decode (ROT13 is symmetric, so the same command works)
./target/release/nightly-rot13-cli "Uryyb, fhesvire!"
# => "Hello, survivor!"
```
If no argument is supplied, the program reads from **STDIN**:
```bash
echo "Secret" | ./target/release/nightly-rot13-cli
# => "Frperg"
```

## Testing
Run the test suite with:
```bash
cargo test
```
All tests are deterministic and run offline.

## License
MIT – see the LICENSE file in the repository root.
