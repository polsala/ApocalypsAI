# nightly-cryptic-qr-encoder

**What it does**

`nightly-cryptic-qr-encoder` is a tiny Rust command‑line utility that takes an arbitrary string and prints a QR code rendered entirely in ASCII characters.  It’s perfect for sharing secret messages on a post‑apocalyptic terminal, embedding URLs in logs, or just having fun with QR art.

**Why Rust?**

The QR generation algorithm is CPU‑intensive but the crate `qrcode` is pure Rust and compiles to a single binary with no external runtime dependencies – ideal for a fast, portable CLI.

**Installation**

```bash
# Clone the repository (or let the ApocalypsAI bot add it under utils/rust-utils/)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-cryptic-qr-encoder

# Build the binary (requires Rust toolchain)
cargo build --release
```

The compiled binary will be located at `target/release/nightly-cryptic-qr-encoder`.

**Usage**

```bash
# Print a QR code for the string "Hello, Wasteland!"
./target/release/nightly-cryptic-qr-encoder "Hello, Wasteland!"
```

The program writes the QR code to standard output using the characters `██` for dark modules and two spaces `  ` for light modules, preserving the square aspect ratio.

**Example output**

```
██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██
██                                                      ██
██  ████  ████  ████  ████  ████  ████  ████  ████  ████  ██
██  ████  ████  ████  ████  ████  ████  ████  ████  ████  ██
... (truncated for brevity) ...
██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██
```

**Testing**

Run the test suite with:

```bash
cargo test --quiet
```

The tests verify that the QR generation function returns a non‑empty string and that the output contains the expected block characters.
