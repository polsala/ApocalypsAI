# Nightly Quantum Entanglement Checker

A whimsical Rust utility that generates and verifies quantum-like entanglement states for fun and testing purposes. Perfect for adding a touch of quantum weirdness to your daily workflow!

## Features

- Generate random quantum entanglement states
- Verify entanglement properties (Bell state checks)
- Calculate quantum fidelity metrics
- Export states to JSON for sharing
- Command-line interface with colorful output

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd <repo-url>

# Build the utility
cargo build --release --bin nightly-quantum-entanglement-checker

# Run the utility
cargo run --release --bin nightly-quantum-entanglement-checker
```

## Usage

```bash
# Generate a random entangled state
./target/release/nightly-quantum-entanglement-checker generate

# Verify a specific state
./target/release/nightly-quantum-entanglement-checker verify --state "|00⟩ + |11⟩"

# Export states to JSON
./target/release/nightly-quantum-entanglement-checker export --count 10 --output states.json

# Check Bell inequality violation
./target/release/nightly-quantum-entanglement-checker bell-test
```

## Examples

### Generate Random States
```bash
cargo run --release --bin nightly-quantum-entanglement-checker generate --count 5
```

### Verify Entanglement
```bash
cargo run --release --bin nightly-quantum-entanglement-checker verify --fidelity 0.95
```

## License

MIT License
