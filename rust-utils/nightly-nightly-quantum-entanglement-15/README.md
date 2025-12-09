# Nightly Quantum Entanglement Checker

A whimsical-yet-useful utility that simulates quantum entanglement between files in your project. When one file changes, its entangled partner(s) are automatically flagged for review!

## Features
- 🚀 Blazing fast Rust implementation
- 🎲 Quantum randomness for entanglement simulation
- 📊 Web dashboard for monitoring entangled pairs
- 🖥️ CLI interface for quick checks
- 🧪 Comprehensive test suite

## Installation

```bash
# Clone this repo and navigate to the utility
cd utils/nightly-quantum-entanglement-checker

# Build with Cargo
cargo build --release

# Or install globally
cargo install --path .
```

## Usage

### CLI Interface

```bash
# Check entanglement status
nightly-quantum-entanglement-checker check --path ./src

# Generate entanglement pairs
nightly-quantum-entanglement-checker generate --path ./src --pairs 5

# Start web dashboard
nightly-quantum-entanglement-checker serve --port 8080
```

### Web Dashboard

1. Start the server: `nightly-quantum-entanglement-checker serve`
2. Open http://localhost:8080 in your browser
3. View real-time entanglement status and statistics

## Quantum Mechanics (The Whimsical Version)

This utility simulates quantum entanglement by:
1. Creating pairs of files that are "quantum-linked"
2. When one file in a pair is modified, its partner becomes "spooky"
3. The web dashboard shows the quantum state of your codebase

## License

MIT License - because quantum physics should be free!

---

*This utility is part of the ApocalypsAI Nightly Integrator project.*
