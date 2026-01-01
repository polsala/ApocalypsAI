# Nightly Quantum Entanglement Checker

A whimsical-yet-useful CLI tool that simulates quantum entanglement verification for distributed systems. Perfect for testing the spooky action at a distance in your microservices!

## Features

- Simulates quantum entanglement verification between distributed nodes
- Generates quantum state reports with measurement probabilities
- Validates entanglement consistency across network partitions
- Provides whimsical quantum-themed output and status messages
- Includes comprehensive test suite with mocked quantum operations

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd utils/nightly-quantum-entanglement-checker

# Build the project
cargo build --release

# Run the binary
cargo run -- --help
```

## Usage

```bash
# Check entanglement between two nodes
./target/release/nightly-quantum-entanglement-checker --node-a service-a --node-b service-b

# Generate quantum state report
./target/release/nightly-quantum-entanglement-checker --report --format json

# Validate entanglement across multiple services
./target/release/nightly-quantum-entanglement-checker --cluster services.txt
```

## Command Line Options

- `--node-a <NAME>`: First node/service name
- `--node-b <NAME>`: Second node/service name
- `--report`: Generate quantum state report
- `--format <FORMAT>`: Output format (json, yaml, text)
- `--cluster <FILE>`: File containing cluster node list
- `--threshold <VALUE>`: Entanglement threshold (0.0-1.0)
- `--help`: Show help message

## Example Output

```
🔬 Quantum Entanglement Verification Report
==========================================

Node A: service-payment-processor
Node B: service-inventory-manager

Entanglement Status: ✅ VERIFIED
Bell State: |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
Fidelity Score: 0.942
Measurement Correlation: 98.7%

Quantum Decoherence Risk: LOW
Recommended Action: Continue spooky action at a distance
```

## Testing

```bash
# Run all tests
cargo test

# Run specific test suite
cargo test quantum_state

# Run with coverage
cargo tarpaulin --out Html
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Submit a pull request

## Quantum Disclaimer

This tool simulates quantum phenomena for entertainment and testing purposes. No actual quantum computers were harmed in the making of this utility.
