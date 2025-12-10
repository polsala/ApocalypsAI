# Nightly Quantum Entanglement Checker

Ever wondered if your code snippets are quantum entangled? This whimsical utility checks if two pieces of code share the same quantum signature (hash) with a playful twist!

## Features

- Generate quantum signatures (SHA-256 hashes) for any code snippet
- Check if two snippets are 'quantum entangled'
- Whimsical quantum-themed output messages
- Cross-platform CLI tool written in Rust

## Installation

### From Source

```bash
# Clone the repository
# Navigate to the utility directory
# Build with Cargo
cargo build --release

# The binary will be at target/release/nightly-quantum-entanglement-checker
```

### Usage

```bash
# Check if two files are quantum entangled
./target/release/nightly-quantum-entanglement-checker file1.rs file2.rs

# Check if two strings are quantum entangled
./target/release/nightly-quantum-entanglement-checker --text "Hello World" "Hello World"

# Generate quantum signature for a single file
./target/release/nightly-quantum-entanglement-checker --signature file.rs

# Generate quantum signature for a text string
./target/release/nightly-quantum-entanglement-checker --signature --text "Hello Quantum World"
```

## Output Examples

```
✨ Quantum Entanglement Detected! ✨

File 1: file1.rs
File 2: file2.rs

Both snippets share the same quantum signature:
315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3

The universe has spoken! 🌌
```

```
❌ Quantum Entanglement Not Found

File 1: file1.rs
File 2: file2.rs

File 1 signature: 315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3
File 2 signature: 7c211433f0207159e71b7252d578f4ee1d3051fe6aa5f22d765a15b0d1775931

These snippets are quantumly independent. 🚀
```

## License

MIT License
