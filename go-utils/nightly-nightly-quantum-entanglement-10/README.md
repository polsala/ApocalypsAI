# Nightly Quantum Entanglement Checker

A whimsical-yet-useful Go utility that simulates quantum entanglement verification for distributed systems. Perfect for testing distributed consensus algorithms, network reliability, and adding a touch of quantum physics to your infrastructure!

## Features

- Simulates quantum entanglement verification between nodes
- Generates entangled particle pairs with correlated states
- Verifies quantum correlation across network boundaries
- Provides statistical analysis of entanglement fidelity
- Includes whimsical quantum-themed logging

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd utils/nightly-quantum-entanglement-checker

# Build the utility
go build -o qentangle src/main.go

# Run the utility
./qentangle --help
```

## Usage

```bash
# Basic entanglement check between two nodes
./qentangle --nodes node1:8080,node2:8080 --particles 1000

# Advanced usage with custom correlation threshold
./qentangle --nodes node1:8080,node2:8080,node3:8080 --particles 5000 --threshold 0.95

# Run in verbose mode for quantum debugging
./qentangle --nodes localhost:9000 --particles 100 --verbose
```

## Output

The utility will display:
- Quantum correlation statistics
- Entanglement fidelity metrics
- Network latency measurements
- Whimsical quantum state descriptions

## Example Output

```
🔬 Initializing quantum entanglement checker...

📡 Establishing quantum links with 2 nodes

⚛️  Generating 1000 entangled particle pairs...

🌀 Measuring quantum correlations...

Results:
- Entanglement Fidelity: 98.7%
- Bell Inequality Violation: 2.71 (Classical limit: 2.0)
- Network Latency: 42ms avg
- Quantum State: "Spooky action at a distance confirmed!"

✅ Quantum entanglement verified across all nodes!
```

## License

MIT License - Use freely, but don't collapse the wave function unnecessarily.
