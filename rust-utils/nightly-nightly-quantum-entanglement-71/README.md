# Nightly Quantum Entanglement Checker

A whimsical-yet-useful CLI tool that simulates quantum entanglement verification for distributed systems. Perfect for testing distributed algorithms, network reliability, and adding some quantum flair to your devops toolkit.

## Features

- Simulates quantum entanglement verification between nodes
- Generates entanglement reports with spooky action metrics
- Supports both local and distributed mode
- Whimsical quantum-themed output
- Cross-platform Rust implementation

## Installation

### From Source

```bash
# Clone the repository
git clone <repo-url>
cd nightly-quantum-entanglement-checker

# Build
cargo build --release

# Install
sudo cp target/release/quantum-entanglement-checker /usr/local/bin/
```

### From Binary

Download the latest release for your platform from the releases page.

## Usage

### Basic Entanglement Check

```bash
# Check entanglement between two local nodes
quantum-entanglement-checker --nodes node1,node2

# Check entanglement with custom entanglement strength
quantum-entanglement-checker --nodes node1,node2 --strength 0.8

# Run in distributed mode with network simulation
quantum-entanglement-checker --nodes node1,node2,node3 --distributed --latency 50ms
```

### Advanced Options

```bash
# Generate detailed entanglement report
quantum-entanglement-checker --nodes node1,node2 --report detailed

# Set custom quantum coherence threshold
quantum-entanglement-checker --nodes node1,node2 --coherence-threshold 0.95

# Run with verbose output
quantum-entanglement-checker --nodes node1,node2 --verbose
```

### Configuration File

Create a `quantum.toml` configuration file:

```toml
[nodes]
primary = "node1"
secondary = "node2"

[quantum]
entanglement_strength = 0.85
coherence_threshold = 0.9
latency_simulation = "100ms"
```

Then run:

```bash
quantum-entanglement-checker --config quantum.toml
```

## Output Examples

### Success Case

```
🔬 Quantum Entanglement Verification Report
==========================================

📍 Nodes: node1 ↔ node2
⚡ Entanglement Strength: 0.85
🔮 Quantum Coherence: 0.92
⏱️  Verification Time: 42ms

✅ ENTANGLEMENT CONFIRMED
"Spooky action at a distance" detected!

📊 Metrics:
  - Bell State Fidelity: 94%
  - Quantum Correlation: 0.87
  - Decoherence Risk: LOW
```

### Failure Case

```
🔬 Quantum Entanglement Verification Report
==========================================

📍 Nodes: node1 ↔ node2
⚡ Entanglement Strength: 0.3
🔮 Quantum Coherence: 0.45
⏱️  Verification Time: 150ms

❌ ENTANGLEMENT FAILED
Quantum decoherence detected!

⚠️  Warning: Measurement collapse probability high

📊 Metrics:
  - Bell State Fidelity: 45%
  - Quantum Correlation: 0.32
  - Decoherence Risk: HIGH
```

## Use Cases

- **Distributed Systems Testing**: Verify node connectivity and synchronization
- **Network Reliability**: Test network latency and packet loss simulation
- **DevOps Tooling**: Add quantum-themed monitoring to your infrastructure
- **Educational**: Learn about quantum mechanics concepts in a fun way
- **Team Building**: Whimsical tool for team challenges and competitions

## Development

### Building

```bash
# Development build
cargo build

# Release build
cargo build --release

# Run tests
cargo test

# Run with example
cargo run -- --nodes test1,test2 --strength 0.9
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Quantum Disclaimer

This tool simulates quantum entanglement for entertainment and testing purposes. No actual quantum particles were harmed in the making of this software. Results may be spooky but are not guaranteed to violate local realism.

## Support

For issues, questions, or quantum-related discussions, please open an issue on the GitHub repository.
