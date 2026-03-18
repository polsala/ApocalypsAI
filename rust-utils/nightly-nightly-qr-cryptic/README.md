# nightly-qr-cryptic

**nightly-qr-cryptic** is a tiny Rust command‑line tool that turns any string into an ASCII QR code that can be displayed directly in a terminal.  For a touch of whimsy you can rotate the QR code by 90° increments.

## Installation

```bash
# Clone the repository and build with Cargo
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-qr-cryptic
cargo build --release
```

The binary will be located at `target/release/nightly-qr-cryptic`.

## Usage

```bash
# Basic QR generation
nightly-qr-cryptic "Hello, world!"

# Rotate the QR code 180° (two 90° turns)
nightly-qr-cryptic "Secret" --rotate 2
```

### Options

- `--rotate N` – Rotate the QR code `N` times by 90° clockwise. `N` must be an integer between 0 and 3 (default: 0).

## How it works

The tool uses the `qrcode` crate to generate a QR matrix, then renders each module as a pair of block characters (`██`) for black and two spaces (`  `) for white.  Rotation is performed on the boolean matrix before rendering.

## Testing

Run the test suite with:

```bash
cargo test
```

The tests verify the rotation logic and ensure the CLI runs without panics.
