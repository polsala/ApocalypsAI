# Nightly Quantum Entanglement Checker

A whimsical-yet-useful CLI tool that simulates quantum entanglement verification for distributed systems using deterministic pseudo-random states.

## Features

- **Entanglement Simulation**: Generates paired quantum states across multiple nodes
- **Bell State Verification**: Validates quantum correlations using CHSH inequality
- **Deterministic Results**: Uses seed-based generation for reproducible testing
- **Performance Metrics**: Measures entanglement verification latency
- **ASCII Visualization**: Displays quantum state correlations in a fun format

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd utils/nightly-quantum-entanglement-checker

# Build with Cargo
cargo build --release

# Run the tool
cargo run --release -- --nodes 4 --trials 1000
```

## Usage

```bash
# Basic entanglement check across 4 nodes
./target/release/nightly-quantum-entanglement-checker --nodes 4 --trials 1000

# Advanced options
./target/release/nightly-quantum-entanglement-checker \
  --nodes 8 \
  --trials 10000 \
  --seed 42 \
  --visualize

# Help
./target/release/nightly-quantum-entanglement-checker --help
```

## Output Example

```
=== Quantum Entanglement Verification ===
Nodes: 4, Trials: 1000, Seed: 12345

Bell State Correlations:
Node A: |0⟩ ⊗ |1⟩ ⊗ |+⟩ ⊗ |-⟩
Node B: |1⟩ ⊗ |0⟩ ⊗ |-⟩ ⊗ |+⟩

CHSH Inequality Test:
S = 2.828 (Classical limit: 2.0, Quantum limit: 2.828)
✓ Entanglement verified! (S > 2.0)

Performance:
Latency: 45ms, Throughput: 22,222 ops/sec
```

## Use Cases

- **Distributed Systems Testing**: Simulate quantum correlations for testing distributed algorithms
- **Educational Tool**: Demonstrate quantum mechanics concepts in a tangible way
- **Performance Benchmarking**: Measure entanglement verification performance across different configurations
- **DevOps Integration**: Include in CI/CD pipelines for quantum-inspired testing

## License

MIT License - see LICENSE file for details.
