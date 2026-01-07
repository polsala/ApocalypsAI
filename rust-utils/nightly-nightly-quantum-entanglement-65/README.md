# Nightly Quantum Entanglement Checker

A whimsical CLI tool that simulates quantum entanglement verification for distributed systems. Perfect for testing the spooky action at a distance in your infrastructure!

## Features

- Simulates quantum entanglement between nodes
- Generates entanglement reports with spooky metrics
- Supports both local and distributed mode
- Whimsical quantum-themed output
- Zero actual quantum physics required

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd nightly-quantum-entanglement-checker

# Build with Cargo
cargo build --release

# Run the tool
cargo run --release -- --help
```

## Usage

### Basic Entanglement Check
```bash
cargo run --release -- check --nodes 3 --distance 100
```

### Distributed Mode
```bash
cargo run --release -- distributed --nodes node1,node2,node3 --correlation 0.8
```

### Generate Report
```bash
cargo run --release -- report --format json --output entanglement_report.json
```

## Options

- `--nodes`: Number of nodes to simulate (default: 3)
- `--distance`: Distance between nodes in quantum units (default: 100)
- `--correlation`: Entanglement correlation strength (0.0-1.0, default: 0.7)
- `--format`: Output format (text, json, yaml)
- `--output`: Output file path
- `--verbose`: Enable verbose quantum logging

## Examples

### Check Local Entanglement
```bash
cargo run --release -- check --nodes 5 --distance 50 --verbose
```

### Generate JSON Report
```bash
cargo run --release -- check --nodes 10 --correlation 0.9 --format json --output spooky_report.json
```

## Quantum Metrics

The tool reports:

- **Entanglement Strength**: How strongly nodes are quantumly linked
- **Spooky Action**: Degree of non-local correlation
- **Decoherence Risk**: Probability of quantum state collapse
- **Superposition Stability**: How well nodes maintain quantum states

## License

MIT License - because quantum physics should be fun for everyone!
