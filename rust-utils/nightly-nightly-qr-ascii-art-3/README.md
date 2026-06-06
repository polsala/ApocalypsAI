# nightly-qr-ascii-art

A tiny Rust CLI that turns any text into an ASCII QR code that can be displayed directly in a terminal.

## Features
- No external image dependencies – output is pure ASCII using `█` and spaces.
- Deterministic rendering; the same input always yields the same QR pattern.
- Small, self‑contained binary (uses the `qrcode` crate only).

## Build & Run
```bash
# Clone the repository (or copy the generated folder) and cd into it
cargo build --release
# Run the binary with the text you want to encode
./target/release/qr-ascii "Hello, world!"
```

The program prints the QR code to stdout. Example:
```
████████████████████████████████
██  ██  ████  ████  ████  ██  ██
██  ██  ████  ████  ████  ██  ██
██  ██  ████  ████  ████  ██  ██
████████████████████████████████
```

## Library API
If you want to embed the functionality in another Rust project, use the `generate_qr_ascii` function from `src/lib.rs`:
```rust
let ascii = qr_ascii_art::generate_qr_ascii("my data");
println!("{}", ascii);
```

## Tests
Run the test suite with:
```bash
cargo test
```
All tests are deterministic and do not require network access.
