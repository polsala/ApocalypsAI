# Nightly Quantum Entanglement Checker

A whimsical-yet-useful utility that simulates quantum entanglement verification for distributed systems. Perfect for testing network reliability and adding some quantum flavor to your infrastructure!

## Features

- Simulates quantum particle pairs across distributed nodes
- Measures "entanglement fidelity" through network round-trips
- Provides real-time visualization dashboard
- Generates quantum-themed reports with actual network metrics

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd nightly-quantum-entanglement-checker

# Build the Rust CLI tool
cargo build --release

# Install the CLI tool
cargo install --path .

# Start the React dashboard
cd dashboard && npm install && npm start
```

## Usage

```bash
# Basic entanglement check between two nodes
nightly-quantum-entanglement-checker --source 192.168.1.100 --target 192.168.1.101

# Advanced mode with custom particle count
nightly-quantum-entanglement-checker --source 192.168.1.100 --target 192.168.1.101 --particles 1000

# Generate quantum report
nightly-quantum-entanglement-checker --report --output quantum_report.json
```

## Dashboard

The React dashboard provides:

- Real-time entanglement fidelity visualization
- Network latency heat maps
- Quantum decoherence alerts
- Historical performance charts

Access at: http://localhost:3000

## License

MIT License - Use responsibly, or irresponsibly, depending on your quantum state.
