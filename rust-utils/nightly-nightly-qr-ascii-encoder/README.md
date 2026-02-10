# nightly-qr-ascii-encoder

A whimsical yet handy Rust command‑line tool that converts a short string into an ASCII‑art QR code that can be displayed directly in a terminal.

## Features
- Zero‑runtime dependencies besides the pure‑Rust `qrcode` crate.
- Outputs QR codes using Unicode block characters for a compact look.
- Works offline – no network calls.

## Installation
```bash
# Clone the utility (or let the ApocalypsAI bot generate it)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-qr-ascii-encoder
cargo build --release
```
The binary will be at `target/release/nightly-qr-ascii-encoder`.

## Usage
```bash
nightly-qr-ascii-encoder "Hello, world!"
```
The program prints the QR code to stdout.

## Example
```
nightly-qr-ascii-encoder "HELLO"
```
```
██  ██  ██  ██
██          ██
  ██  ██  ██  
██  ██  ██  ██
```
*(actual output may vary slightly depending on terminal font)*

## Testing
Run the bundled tests with:
```bash
cargo test
```
All tests are deterministic and run offline.
