# Nightly Quantum Entanglement Checker

Ever wondered if your code files are quantum-entangled across the multiverse? This whimsical-yet-useful tool checks if two files share the same quantum state (hash) with a probabilistic twist!

## Features

- 🚀 Fast Rust implementation with SHA-256 hashing
- 🌀 Quantum metaphor with "probability waves" and "entanglement"
- 🎲 Probabilistic output that adds quantum uncertainty
- 📊 Detailed comparison report
- 🧪 Comprehensive test suite

## Installation

```bash
cargo build --release
```

## Usage

```bash
# Check if two files are quantum-entangled
cargo run --release -- --file1 path/to/file1.txt --file2 path/to/file2.txt

# With custom probability threshold (0.0-1.0)
cargo run --release -- --file1 path/to/file1.txt --file2 path/to/file2.txt --threshold 0.8

# Verbose output with quantum state details
cargo run --release -- --file1 path/to/file1.txt --file2 path/to/file2.txt --verbose
```

## Example Output

```
🔬 Quantum Entanglement Analysis
================================

File 1: src/main.rs
  📏 Size: 1,234 bytes
  🌀 Quantum State: a1b2c3d4e5f6...
  ⚡ Energy Level: High

File 2: src/main_copy.rs
  📏 Size: 1,234 bytes
  🌀 Quantum State: a1b2c3d4e5f6...
  ⚡ Energy Level: High

🔮 Entanglement Probability: 99.7%
✅ Quantum States Match!
🎉 Files are quantum-entangled!
```

## Quantum Mechanics Explained

In our quantum universe:
- **Quantum State** = SHA-256 hash of the file
- **Energy Level** = File size category (Low/Medium/High)
- **Entanglement Probability** = 100% if hashes match, otherwise random (quantum uncertainty!)

## License

MIT License - because quantum physics should be free for everyone!
