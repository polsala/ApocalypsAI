# Nightly Quantum Entanglement Checker

Ever wondered if your code changes are quantumly entangled? This tool simulates quantum entanglement between files to detect if changes are "spookily connected" across your codebase.

## Features

- 🌀 Simulates quantum superposition states for files
- 🎯 Detects entanglement correlations between file changes
- 📊 Generates spooky action reports
- 🧪 Includes quantum decoherence testing
- 🎲 Uses true randomness for quantum simulation

## Installation

```bash
# Clone the repo and navigate to the utility
cd utils/nightly-quantum-entanglement-checker

# Build the Rust binary
cargo build --release

# Run the entanglement checker
./target/release/quantum-entanglement-checker --help
```

## Usage

```bash
# Check entanglement between two files
./target/release/quantum-entanglement-checker check file1.rs file2.rs

# Generate entanglement report for a directory
./target/release/quantum-entanglement-checker report src/

# Test quantum decoherence with multiple files
./target/release/quantum-entanglement-checker decoherence file1.rs file2.rs file3.rs
```

## Quantum States Explained

- **Superposition**: Files exist in multiple states until observed
- **Entanglement**: Changes to one file affect its entangled partner
- **Decoherence**: Measurement collapses quantum states to classical reality
- **Bell States**: Maximum entanglement configurations

## Example Output

```
🔬 Quantum Entanglement Analysis Report
========================================

File A: src/main.rs
File B: src/lib.rs

Quantum Correlation Score: 0.842
Entanglement Status: ✨ STRONGLY ENTANGLED

Bell State: |Ψ⁻⟩ (Singlet State)
Decoherence Risk: LOW
Spooky Action: CONFIRMED 🎃

Recommendation: These files should be modified together for optimal quantum harmony.
```

## License

MIT License - because quantum physics is free for everyone!
