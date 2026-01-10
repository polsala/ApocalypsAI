# Nightly Quantum Entanglement Checker

A whimsical-yet-useful Rust CLI tool that simulates quantum entanglement verification for distributed systems. Perfect for testing distributed system resilience and adding some quantum flavor to your workflow!

## Features

- Simulates quantum entanglement verification between nodes
- Generates mock quantum states with entanglement properties
- Validates entanglement consistency across distributed nodes
- Provides quantum-themed output and metrics
- Includes comprehensive test suite with mocked quantum operations

## Installation

### From Source

```bash
# Clone the repository
# Navigate to the quantum-entanglement-checker directory
# Build the project
cargo build --release

# Run the tool
cargo run --release -- --help
```

### Binary Usage

```bash
# After building, use the binary directly
target/release/nightly-quantum-entanglement-checker --help
```

## Usage

```bash
# Basic entanglement check between two nodes
nightly-quantum-entanglement-checker check --node-a node1 --node-b node2

# Check entanglement with custom quantum state size
nightly-quantum-entanglement-checker check --node-a node1 --node-b node2 --state-size 1024

# Generate quantum metrics report
nightly-quantum-entanglement-checker metrics --node-count 5 --duration 30

# Verify entanglement across multiple nodes
nightly-quantum-entanglement-checker verify --nodes node1,node2,node3,node4,node5
```

## Commands

- `check`: Verify entanglement between two specific nodes
- `metrics`: Generate quantum metrics across multiple nodes
- `verify`: Validate entanglement across a cluster of nodes
- `simulate`: Run a full quantum simulation with configurable parameters

## Options

- `--node-a`, `--node-b`: Specify nodes for pairwise checking
- `--nodes`: Comma-separated list of nodes for cluster verification
- `--state-size`: Size of quantum states (default: 512)
- `--duration`: Simulation duration in seconds (default: 10)
- `--node-count`: Number of nodes for metrics generation
- `--verbose`: Enable verbose quantum state output
- `--help`: Show help information

## Quantum Concepts

This tool simulates:

- **Quantum Superposition**: States exist in multiple configurations simultaneously
- **Quantum Entanglement**: Correlated states between distributed nodes
- **Quantum Decoherence**: Loss of quantum properties over time
- **Bell State Verification**: Testing entanglement quality

## Examples

### Basic Node Pair Check

```bash
nightly-quantum-entanglement-checker check --node-a alpha --node-b beta --verbose
```

### Cluster Verification

```bash
nightly-quantum-entanglement-checker verify --nodes server1,server2,server3,server4,server5
```

### Performance Metrics

```bash
nightly-quantum-entanglement-checker metrics --node-count 10 --duration 60 --state-size 2048
```

## Testing

Run the comprehensive test suite:

```bash
cargo test
cargo test -- --nocapture  # For verbose output
```

## License

MIT License - feel free to use in your quantum computing projects!

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Quantum Disclaimer

This tool simulates quantum concepts for entertainment and educational purposes. It does not perform actual quantum computing operations.
