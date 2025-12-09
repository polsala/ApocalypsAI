# Nightly Quantum Entanglement Checker

Ever wondered if your code files are quantum-entangled across the multiverse? This whimsical-yet-useful utility checks if two files share the same quantum state (hash) with a probabilistic twist!

## Features

- 🚀 Fast Rust implementation with Blake3 hashing
- 🌀 Quantum probability simulation (99.7% confidence)
- 📊 Detailed entanglement report
- 🎲 Random quantum noise injection for fun
- 🧪 Comprehensive test suite

## Installation

```bash
# Clone the repo and navigate to the utility
cd utils/nightly-quantum-entanglement-checker

# Build with Cargo
cargo build --release
```

## Usage

```bash
# Check if two files are quantum-entangled
cargo run --release -- --file1 path/to/file1 --file2 path/to/file2

# With custom probability threshold (0.0-1.0)
cargo run --release -- --file1 path/to/file1 --file2 path/to/file2 --threshold 0.95

# Verbose output
cargo run --release -- --file1 path/to/file1 --file2 path/to/file2 --verbose
```

## Example Output

```
🔬 Quantum Entanglement Analysis Report
=====================================

File 1: src/main.rs
File 2: src/main_copy.rs

Hash 1: a1b2c3d4e5f6...
Hash 2: a1b2c3d4e5f6...

Quantum State: IDENTICAL
Probability: 99.7%
Quantum Noise: 0.0003

🎉 CONCLUSION: These files are quantum-entangled!

Note: This entanglement may or may not violate the no-cloning theorem.
```

## License

MIT License - Use freely, but don't blame us if you create a quantum paradox!
