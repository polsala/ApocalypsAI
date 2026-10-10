# nightly-entropy-analyzer

**nightly-entropy-analyzer** is a whimsical yet practical Rust command‑line tool that calculates the Shannon entropy of a given input.  Entropy is a measure of randomness – useful for checking password strength, evaluating compression potential, or just satisfying post‑apocalyptic curiosity about data unpredictability.

## Features

- Accepts a file path argument or reads from **STDIN** when no argument is supplied.
- Outputs the entropy in bits per byte with four decimal places.
- Zero external dependencies – pure Rust standard library.
- Includes a deterministic test suite that runs with `cargo test`.

## Build & Install

```bash
# Clone the repository (or copy the generated folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd rust-utils/nightly-entropy-analyzer

# Build the binary
cargo build --release

# Run the tool
./target/release/entropy-analyzer path/to/file.txt
# Or pipe data
cat file.txt | ./target/release/entropy-analyzer
```

## Usage

```text
USAGE:
    entropy-analyzer [FILE]

ARGS:
    <FILE>    Optional path to a file. If omitted, reads from STDIN.
```

## Example

```bash
$ echo -n "aaaaabbbbcc" | ./target/release/entropy-analyzer
Entropy: 1.4930 bits/byte
```

## Testing

Run the built‑in tests with:

```bash
cargo test --quiet
```

The test suite uses a hard‑coded string and verifies the computed entropy against a known value.
