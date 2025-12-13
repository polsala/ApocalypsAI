# Nightly Quantum Entanglement Checker

A whimsical utility that checks if two code snippets are 'quantum entangled' by comparing their hash signatures with a playful twist.

## Features

- 🚀 Fast Rust implementation for lightning-quick comparisons
- 🌀 Quantum-themed output with probability percentages
- 🎭 Whimsical messages for different entanglement levels
- 🔒 Cryptographically secure hashing (SHA-256)
- 📝 Detailed comparison reports

## Installation

```bash
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI

# Build the Rust utility
cargo build --release --bin nightly-quantum-entanglement-checker
```

## Usage

```bash
# Compare two files
./target/release/nightly-quantum-entanglement-checker file1.rs file2.rs

# Compare file contents with stdin
echo "fn main() {}" | ./target/release/nightly-quantum-entanglement-checker file1.rs -

# Generate detailed report
./target/release/nightly-quantum-entanglement-checker --report file1.rs file2.rs
```

## Output Example

```
Quantum Entanglement Analysis Report
==================================

File A: src/main.rs
File B: src/backup.rs

Entanglement Probability: 97.3%

Status: 🌀 QUANTUM ENTANGLEMENT DETECTED!

The wave functions of these code snippets have collapsed into remarkably similar states.
This suggests they share a common quantum origin or have been observed too many times.

Recommendation: These files are practically twins. Consider merging or documenting their relationship.
```

## Entanglement Levels

- **0-20%**: "Cosmic Background Radiation" - No meaningful connection
- **21-40%**: "Stellar Drift" - Slight similarities, likely coincidental
- **41-60%**: "Orbital Resonance" - Noticeable patterns, worth investigating
- **61-80%**: "Gravitational Pull" - Strong similarities, likely related
- **81-100%**: "Quantum Entanglement" - Nearly identical, definitely related

## License

MIT License - see LICENSE file for details.
