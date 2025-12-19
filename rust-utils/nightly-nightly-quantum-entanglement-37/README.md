# Nightly Quantum Entanglement Checker

A whimsical-yet-useful utility that simulates quantum entanglement verification for distributed systems. Perfect for testing distributed consensus algorithms, network reliability, and adding some quantum flavor to your infrastructure!

## Features

- Simulates quantum entanglement verification between nodes
- Measures "quantum coherence" across distributed systems
- Provides whimsical quantum-themed status reports
- Fast, async Rust implementation with zero runtime dependencies
- Includes comprehensive tests with deterministic mocking

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd <repo-url>/rust-utils/nightly-quantum-entanglement-checker

# Build the project
cargo build --release

# Run the checker
cargo run --release -- --nodes 5 --distance 1000
```

## Usage

```bash
# Basic usage with default settings
cargo run --

# Custom configuration
cargo run -- --nodes 10 --distance 5000 --threshold 0.8

# Help
cargo run -- --help
```

## Command Line Options

- `--nodes` or `-n`: Number of simulated nodes (default: 5)
- `--distance` or `-d`: Distance between nodes in kilometers (default: 1000)
- `--threshold` or `-t`: Entanglement threshold (0.0-1.0, default: 0.7)
- `--help` or `-h`: Show help information

## Example Output

```
🔬 Quantum Entanglement Checker Initializing...

📡 Establishing quantum links between 5 nodes...
📍 Node positions: [0km, 1000km, 2000km, 3000km, 4000km]

🧪 Running entanglement verification...

Node 0 ↔ Node 1: ✨ ENTANGLED (coherence: 0.85)
Node 0 ↔ Node 2: ⚠️  WEAK (coherence: 0.62)
Node 0 ↔ Node 3: ❌ BROKEN (coherence: 0.34)
Node 0 ↔ Node 4: ⚠️  WEAK (coherence: 0.58)

Overall quantum network health: 55% ✨
Recommendation: Deploy quantum repeaters for better coherence!
```

## Technical Details

This utility simulates quantum entanglement using:

- **Distance-based decay**: Entanglement strength decreases with distance
- **Random quantum noise**: Simulates real-world quantum decoherence
- **Async verification**: Concurrent checking of all node pairs
- **Deterministic results**: Uses seeded RNG for reproducible tests

## Testing

```bash
# Run all tests
cargo test

# Run specific test
cargo test test_entanglement_decay

# Run with coverage (if available)
cargo tarpaulin
```

## License

MIT License - feel free to use in your quantum computing projects!

---

*Note: This is a simulation for entertainment and educational purposes. Actual quantum entanglement may require cryogenic temperatures and expensive equipment.*
