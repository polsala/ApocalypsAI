# Nightly Quantum Entanglement Checker

A whimsical-yet-useful utility that simulates quantum entanglement verification for distributed systems. Perfect for testing network reliability and demonstrating quantum computing concepts in a fun way!

## Features
- Simulates quantum particle entanglement across network nodes
- Measures "quantum coherence" between distributed components
- Provides whimsical quantum-themed status reports
- Useful for testing network latency and reliability
- Rust async implementation for high performance

## Installation

Requires Rust 1.70+:

```bash
# Clone and build
git clone <repo-url>
cd nightly-quantum-entanglement-checker
cargo build --release
```

## Usage

```bash
# Basic entanglement check
cargo run -- --nodes 192.168.1.100,192.168.1.101,192.168.1.102

# Advanced options
cargo run -- --nodes 192.168.1.100,192.168.1.101 --threshold 0.7 --timeout 5000

# Help
cargo run -- --help
```

## Output

```
🔬 Quantum Entanglement Checker v1.0
=====================================

📡 Spooky action at a distance detected!

Node: 192.168.1.100
  - Quantum coherence: 0.842 (84.2%)
  - Entanglement status: ✨ SUPERPOSED
  - Measurement collapsed: No

Node: 192.168.1.101
  - Quantum coherence: 0.839 (83.9%)
  - Entanglement status: ✨ SUPERPOSED
  - Measurement collapsed: No

Node: 192.168.1.102
  - Quantum coherence: 0.845 (84.5%)
  - Entanglement status: ✨ SUPERPOSED
  - Measurement collapsed: No

🎉 Overall system entanglement: 84.2% (STABLE)
```

## License

MIT License - feel free to use in your quantum experiments!
