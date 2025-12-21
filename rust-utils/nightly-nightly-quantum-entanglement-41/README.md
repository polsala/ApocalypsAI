# Nightly Quantum Entanglement Checker

A whimsical CLI tool that simulates quantum entanglement verification for distributed systems. Perfect for testing the spooky action at a distance in your microservices!

## Features

- Simulates quantum entanglement verification between distributed nodes
- Generates quantum state correlations with configurable decoherence
- Provides whimsical quantum physics-themed output
- Cross-platform Rust binary with no external dependencies
- Includes comprehensive tests with mocked quantum states

## Installation

### From Source (Recommended)
```bash
# Clone the repository
# Navigate to the rust-utils/nightly-quantum-entanglement-checker directory

# Build the project
cargo build --release

# Run the binary
./target/release/nightly-quantum-entanglement-checker --help
```

### From Pre-built Binary
```bash
# Download the latest release for your platform
# Extract and run
```

## Usage

```bash
# Basic entanglement check between two nodes
nightly-quantum-entanglement-checker --node-a "Alpha" --node-b "Beta"

# Advanced usage with custom parameters
nightly-quantum-entanglement-checker \
  --node-a "Server-01" \
  --node-b "Server-02" \
  --decoherence 0.15 \
  --measurements 1000 \
  --verbose

# Check entanglement across multiple node pairs
nightly-quantum-entanglement-checker \
  --node-a "Alpha" --node-b "Beta" \
  --node-a "Gamma" --node-b "Delta" \
  --batch-mode
```

## Command Line Options

- `--node-a <NAME>`: Name of the first quantum node (required)
- `--node-b <NAME>`: Name of the second quantum node (required)
- `--decoherence <VALUE>`: Decoherence factor (0.0 to 1.0, default: 0.1)
- `--measurements <COUNT>`: Number of quantum measurements to simulate (default: 100)
- `--batch-mode`: Process multiple node pairs in sequence
- `--verbose`: Show detailed quantum state information
- `--help`: Show help message

## Quantum Physics Concepts Simulated

- **Superposition**: Nodes exist in multiple states simultaneously until measured
- **Entanglement**: Measurement of one node instantly affects its entangled partner
- **Decoherence**: Environmental interference that breaks quantum states
- **Bell Inequality**: Statistical test to verify genuine quantum entanglement

## Example Output

```
🔬 Quantum Entanglement Verification Protocol
==========================================

📡 Node A: "Alpha" (Qubit ID: Q-α-7f3c9a)
📡 Node B: "Beta"  (Qubit ID: Q-β-2e8d4b)

🧪 Initializing quantum superposition...
✨ Entangling qubits via quantum teleportation...

📊 Running 1000 quantum measurements...

Results:
- Correlation coefficient: 0.942
- Bell inequality violation: 2.37 (threshold: 2.0)
- Decoherence factor: 0.10
- Entanglement status: ✅ VERIFIED

🎉 Spooky action at a distance confirmed!
```

## Testing

Run the comprehensive test suite:

```bash
cargo test
```

The tests include:
- Quantum state generation and validation
- Entanglement correlation calculations
- Decoherence effect simulation
- Bell inequality verification
- Error handling for invalid inputs

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/quantum-improvements`
3. Commit your changes: `git commit -m 'Add quantum optimization'`
4. Push to the branch: `git push origin feature/quantum-improvements`
5. Open a Pull Request

## License

MIT License - see LICENSE file for details.

## Quantum Disclaimer

⚠️ **Important**: This tool simulates quantum physics concepts for entertainment and educational purposes. It does not perform actual quantum computing operations. Any resemblance to real quantum phenomena is purely coincidental and intended to be whimsical.

## Acknowledgments

- Schrödinger for the cat
- Einstein for the "spooky action"
- Bell for the inequality
- All quantum physicists who made this whimsical tool possible
