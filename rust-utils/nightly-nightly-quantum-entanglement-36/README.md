# Nightly Quantum Entanglement Checker

A whimsical-yet-useful utility that simulates quantum entanglement verification for distributed systems. Perfect for testing distributed consensus algorithms and understanding quantum-inspired computing concepts!

## Features

- Simulates quantum entanglement verification between nodes
- Generates quantum state measurements with proper statistical distributions
- Provides entanglement fidelity metrics
- Includes spooky action at a distance detection
- Whimsical quantum-themed output messages

## Installation

```bash
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git

cd ApocalypsAI/rust-utils/nightly-quantum-entanglement-checker

# Build the project
cargo build --release

# Run the entanglement checker
./target/release/nightly-quantum-entanglement-checker --nodes 4 --measurements 1000
```

## Usage

```bash
# Basic usage with default settings
./target/release/nightly-quantum-entanglement-checker

# Custom configuration
./target/release/nightly-quantum-entanglement-checker \
  --nodes 8 \
  --measurements 5000 \
  --fidelity-threshold 0.85 \
  --output-format json

# Help
./target/release/nightly-quantum-entanglement-checker --help
```

## Output Example

```
🌌 Quantum Entanglement Verification Report 🌌

Nodes: 4 | Measurements: 1000 | Fidelity Threshold: 0.80

📊 Entanglement Fidelity Scores:
• Node 0 ↔ Node 1: 0.923 ✨ (Strongly entangled)
• Node 0 ↔ Node 2: 0.456 ❌ (Not entangled)
• Node 0 ↔ Node 3: 0.887 ✨ (Strongly entangled)
• Node 1 ↔ Node 2: 0.321 ❌ (Not entangled)
• Node 1 ↔ Node 3: 0.945 ✨ (Strongly entangled)
• Node 2 ↔ Node 3: 0.234 ❌ (Not entangled)

🔮 Spooky Action Detected: 3 pairs
⚠️  Classical Correlation: 3 pairs

🎉 Overall System Entanglement: 50.0% (3/6 pairs entangled)

"The universe is not only stranger than we imagine,
 it is stranger than we *can* imagine." - J.B.S. Haldane
```

## Algorithm Details

This utility implements a simplified quantum entanglement simulation using:

1. **Bell State Preparation**: Creates entangled qubit pairs using Hadamard and CNOT gates
2. **Measurement Bases**: Randomly selects measurement bases for each node
3. **Correlation Analysis**: Calculates Pearson correlation coefficients between measurement outcomes
4. **Fidelity Calculation**: Determines entanglement strength based on quantum mechanical predictions

## Use Cases

- Educational tool for quantum computing concepts
- Testing distributed system synchronization
- Simulating quantum-inspired algorithms
- Whimsical team building exercises
- Understanding quantum mechanics principles

## License

MIT License - see LICENSE file for details.

---

*Note: This is a simulation for educational and entertainment purposes. 
Real quantum entanglement requires actual quantum hardware.*
