# Nightly Quantum Entanglement Checker

A whimsical-yet-useful Rust CLI tool that simulates quantum entanglement verification for distributed systems. Perfect for testing distributed algorithms, understanding quantum concepts, or just adding some quantum flair to your development workflow.

## Features

- Simulates quantum entanglement between distributed nodes
- Generates Bell state measurements
- Calculates entanglement fidelity
- Visualizes quantum state correlations
- Export results to JSON for analysis

## Installation

### From Crates.io
```bash
cargo install nightly-quantum-entanglement-checker
```

### From Source
```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-quantum-entanglement-checker
cargo build --release
```

## Usage

### Basic Entanglement Check
```bash
nightly-quantum-entanglement-checker check --nodes 4 --iterations 1000
```

### Advanced Simulation
```bash
nightly-quantum-entanglement-checker simulate --nodes 8 --fidelity 0.95 --output results.json
```

### Bell State Analysis
```bash
nightly-quantum-entanglement-checker analyze --state "|00⟩ + |11⟩" --measurements 500
```

## Commands

- `check`: Run basic entanglement verification
- `simulate`: Run advanced quantum simulation with custom parameters
- `analyze`: Analyze specific quantum states and measurements
- `help`: Show help information

## Options

- `--nodes`: Number of simulated quantum nodes (2-16)
- `--iterations`: Number of measurement iterations (100-10000)
- `--fidelity`: Target entanglement fidelity (0.0-1.0)
- `--state`: Quantum state to analyze (e.g., "|00⟩ + |11⟩")
- `--output`: Output file for results (JSON format)
- `--verbose`: Enable detailed output

## Examples

### Testing Distributed System Synchronization
```bash
# Simulate 8 nodes with high fidelity entanglement
nightly-quantum-entanglement-checker simulate --nodes 8 --fidelity 0.98 --iterations 2000
```

### Educational Quantum Computing
```bash
# Analyze Bell state measurements
nightly-quantum-entanglement-checker analyze --state "|00⟩ + |11⟩" --measurements 1000 --verbose
```

### Performance Benchmarking
```bash
# Quick entanglement check for CI/CD
nightly-quantum-entanglement-checker check --nodes 4 --iterations 500
```

## Output Format

Results are displayed in a human-readable format and can be exported to JSON:

```json
{
  "nodes": 4,
  "iterations": 1000,
  "fidelity": 0.945,
  "correlations": {
    "perfect": 850,
    "imperfect": 150
  },
  "bell_inequality_violation": 2.34,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Quantum Concepts Explained

- **Entanglement**: Quantum correlation between particles
- **Bell State**: Maximally entangled two-qubit state
- **Fidelity**: Measure of quantum state accuracy
- **Bell Inequality**: Test for quantum vs classical behavior

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Submit a pull request

## Disclaimer

This tool simulates quantum phenomena for educational and testing purposes. It does not perform actual quantum computing operations.
