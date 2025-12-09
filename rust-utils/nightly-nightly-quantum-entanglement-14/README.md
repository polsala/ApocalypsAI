# Nightly Quantum Entanglement Checker

A whimsical CLI tool that checks if two code snippets are 'quantum entangled' by comparing their hash signatures with a touch of quantum randomness.

## Features

- 🚀 Fast Rust implementation with zero dependencies
- 🔬 Quantum-inspired randomness for fun comparisons
- 📊 Detailed entanglement reports
- 🎲 Optional quantum decoherence simulation
- 🧪 Comprehensive test suite with deterministic mocks

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd utils/nightly-quantum-entanglement-checker

# Build the project
cargo build --release

# Run the CLI
cargo run --release -- --help
```

## Usage

```bash
# Check entanglement between two files
cargo run --release -- check --file1 code1.rs --file2 code2.rs

# Check entanglement with quantum decoherence
cargo run --release -- check --file1 code1.rs --file2 code2.rs --decoherence 0.1

# Generate quantum report
cargo run --release -- report --file1 code1.rs --file2 code2.rs --output report.json
```

## Example Output

```
🔬 Quantum Entanglement Analysis Report
=====================================

File 1: code1.rs
File 2: code2.rs

Quantum State: Superposition Detected ✓
Entanglement Level: 87.4%
Quantum Coherence: Stable

Probability of Quantum Tunneling: 12.6%
Decoherence Factor: 0.0

Conclusion: These code snippets are quantumly entangled!
```

## License

MIT License - feel free to use in your quantum computing projects!
