# Apocalypse QR

**nightly‑apocalypse‑qr** – a tiny Rust CLI that turns any text into a QR code rendered as ASCII art.  For extra flair you can wrap the output in a radiation‑symbol border, perfect for those end‑of‑the‑world notes.

## Installation

```bash
# Clone the utility (or let the ApocalypsAI agent add it to the repo)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-apocalypse-qr

# Build the binary
cargo build --release
```

The compiled binary will be at `target/release/nightly-apocalypse-qr`.

## Usage

```bash
# Basic QR code
nightly-apocalypse-qr "Hello, world!"

# QR code with radiation border
nightly-apocalypse-qr "Hello, world!" --radiation
```

### Options

- `--radiation` – Wrap the ASCII QR in a decorative radiation‑symbol border.

## Example Output

```text
█░█░█░█░█░█░█░█░█
░█░░█░░█░░█░░█░░
█░█░█░█░█░█░█░█░
... (truncated)
```

When `--radiation` is used, the output is surrounded by `☢` symbols.

## Testing

Run the test suite with:

```bash
cargo test
```

The tests verify that the radiation border is correctly added and that the QR generation does not panic.
