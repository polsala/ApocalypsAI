# Nightly Quantum Entanglement Checker

A whimsical-yet-useful utility that simulates quantum entanglement verification for distributed systems. Perfect for testing network reliability and demonstrating quantum computing concepts!

## Features

- Simulates quantum entanglement between two nodes
- Measures "quantum correlation" using random number generation
- Provides spooky action at a distance metrics
- Cross-platform Rust implementation with async support
- Includes comprehensive tests with deterministic mocking

## Installation

Requires Rust 1.70+:

```bash
# Clone and build
cargo build --release

# Run the simulation
./target/release/nightly-quantum-entanglement-checker
```

## Usage

```bash
# Basic entanglement check
quantum-entanglement-checker --nodes 2 --duration 5

# Advanced options
quantum-entanglement-checker --nodes 4 --duration 10 --correlation-threshold 0.8
```

## Output

```
🔬 Quantum Entanglement Simulation Starting...

📡 Initializing 2 entangled nodes...
⏱️  Running for 5 seconds...

🔮 Measuring quantum correlations...

Node A: [↑][↓][↑][↑][↓]
Node B: [↓][↑][↓][↓][↑]

✅ Entanglement verified! Correlation: 1.00
🎉 Spooky action at a distance confirmed!
```

## License

MIT License - feel free to use for both classical and quantum computing projects!
