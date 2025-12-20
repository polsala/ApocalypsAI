# Nightly Quantum Entanglement Checker

A whimsical-yet-useful CLI tool that generates quantum-entangled hash pairs for secure data synchronization. Perfect for ensuring two files are perfectly synchronized across the multiverse!

## Features

- Generate entangled SHA-256 hash pairs for any file
- Verify entanglement between two files
- Whimsical quantum-themed output
- Fast Rust implementation with zero dependencies

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd <repo-url>/rust-utils/nightly-quantum-entanglement-checker

# Build the tool
cargo build --release

# Run the binary
cargo run --release --
```

## Usage

### Generate Entangled Hashes
```bash
cargo run --release -- generate --file path/to/file.txt
```

### Verify Entanglement
```bash
cargo run --release -- verify --file1 path/to/file1.txt --file2 path/to/file2.txt --hash1 <hash1> --hash2 <hash2>
```

## Example Output
```
🔬 Quantum Entanglement Checker v1.0.0

Generating entangled hashes for: document.pdf

✨ Quantum state observed!
Hash 1: a1b2c3d4e5f67890...
Hash 2: 0987654321fedcba...

These hashes are now quantum-entangled across dimensions!
```

## License

MIT License - feel free to use in your post-apocalyptic projects.
