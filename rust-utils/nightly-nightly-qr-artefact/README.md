# nightly‑qr‑artefact

**What it does**

`nightly‑qr‑artefact` is a small, zero‑dependency (aside from the pure‑Rust `qrcodegen` crate) command‑line tool that converts an arbitrary string into a QR‑code rendered as ASCII art.  The output can be copied‑and‑pasted into any terminal, chat, or markdown document.

**Why it’s useful**

* Share URLs, passwords, or any short text without leaving your terminal.
* No external image viewers – the QR‑code is pure text.
* Fun for demos, teaching, or just impressing friends.

**Installation**

```bash
# Clone the repository (or let the ApocalypsAI bot add it under rust‑utils/)
git clone https://github.com/polsala/ApocalypsAI.git
cd rust-utils/nightly-qr-artefact

# Build the binary
cargo build --release
```

**Usage**

```bash
# Print the QR‑code for a string (e.g., a URL)
cargo run --release -- "https://example.com"
```

The program writes the QR‑code to STDOUT.  Each black module is rendered as `██` and each white module as two spaces, preserving the square aspect ratio.

**Example output**

```
████████████████████████████████
██  ██  ██  ██  ██  ██  ██  ██
██  ████  ████  ████  ████  ██
██  ██  ██  ██  ██  ██  ██  ██
████████████████████████████████
```

*(The actual pattern will differ based on the input string.)*

**Testing**

Run the bundled tests with:

```bash
cargo test --quiet
```

The tests verify that the same input always yields the same ASCII output and that different inputs produce different outputs.
