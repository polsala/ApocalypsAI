# Nightly Quantum Entanglement Checker

A whimsical-yet-practical Rust CLI tool that simulates quantum entanglement verification for distributed systems. Perfect for testing distributed consensus algorithms, network reliability, and adding some quantum flair to your devops toolkit.

## Features

- Simulates quantum entanglement verification between nodes
- Generates entanglement reports with statistical analysis
- Supports both local and distributed mode
- Configurable entanglement strength and decoherence rates
- JSON output for integration with monitoring systems

## Installation

### From Source
```bash
# Clone the repository
# Navigate to the rust-utils/nightly-quantum-entanglement-checker directory
# Build the project
cargo build --release

# Run the tool
./target/release/nightly-quantum-entanglement-checker --help
```

### From Crates.io (when published)
```bash
cargo install nightly-quantum-entanglement-checker
```

## Usage

### Basic Usage
```bash
# Check entanglement between two nodes
nightly-quantum-entanglement-checker --node-a node1 --node-b node2

# Check entanglement with custom parameters
nightly-quantum-entanglement-checker --node-a node1 --node-b node2 --strength 0.8 --decoherence 0.1
```

### Distributed Mode
```bash
# Check entanglement across multiple nodes
nightly-quantum-entanglement-checker --distributed --nodes node1,node2,node3,node4

# Output results in JSON format
nightly-quantum-entanglement-checker --distributed --nodes node1,node2,node3 --format json
```

### Configuration File
```bash
# Use a configuration file
nightly-quantum-entanglement-checker --config config.toml
```

## Configuration File Format

```toml
[node_a]
name = "primary-node"
address = "192.168.1.100"

[node_b]
name = "secondary-node"
address = "192.168.1.101"

[quantum]
strength = 0.95
decoherence = 0.05
measurement_precision = 0.001

[output]
format = "json"
verbose = true
```

## Output Formats

### Text Output
```
Quantum Entanglement Verification Report
======================================

Node A: node1
Node B: node2

Entanglement Strength: 0.85
Decoherence Rate: 0.12
Measurement Precision: 0.001

Status: ENTANGLED ✓
Confidence: 94.2%

Recommendation: System is stable. No quantum corrections required.
```

### JSON Output
```json
{
  "node_a": "node1",
  "node_b": "node2",
  "entanglement_strength": 0.85,
  "decoherence_rate": 0.12,
  "measurement_precision": 0.001,
  "status": "ENTANGLED",
  "confidence": 0.942,
  "recommendation": "System is stable. No quantum corrections required.",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Use Cases

1. **Distributed Systems Testing**: Verify that your distributed systems maintain proper synchronization
2. **Network Reliability**: Test network connections and latency under various conditions
3. **DevOps Monitoring**: Add quantum-themed monitoring to your infrastructure
4. **Educational Tool**: Learn about quantum mechanics concepts through simulation
5. **Team Building**: Fun way to check if team members are "on the same wavelength"

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Submit a pull request

## Disclaimer

This tool is a simulation and does not perform actual quantum entanglement. It's designed for educational and entertainment purposes while providing practical utility for distributed systems testing.
