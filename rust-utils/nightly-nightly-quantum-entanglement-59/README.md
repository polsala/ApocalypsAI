# Nightly Quantum Entanglement Simulator

A whimsical quantum entanglement simulator that generates spooky correlations for testing distributed systems. Perfect for testing distributed systems that need to handle quantum-like spooky action at a distance!

## Features

- Generates entangled particle pairs with correlated properties
- Simulates quantum decoherence and measurement collapse
- Provides spooky correlation statistics
- Cross-platform Rust implementation
- Zero external dependencies

## Usage

```bash
# Build the simulator
cargo build --release

# Run the simulator
./target/release/nightly-quantum-entanglement-simulator

# Generate 1000 entangled pairs
./target/release/nightly-quantum-entanglement-simulator --pairs 1000

# Measure with specific basis
./target/release/nightly-quantum-entanglement-simulator --basis 45 --pairs 500
```

## Output

The simulator outputs entangled particle pairs with their measurement results:

```
Generating 100 entangled particle pairs...

Particle A: Spin=Up, Polarization=Horizontal, Measurement=+1
Particle B: Spin=Down, Polarization=Vertical, Measurement=-1
Correlation: Perfect anti-correlation (spooky!)

...

Summary Statistics:
- Total pairs: 100
- Perfect correlations: 95 (95.0%)
- Imperfect correlations: 5 (5.0%)
- Average decoherence time: 0.023 seconds
```

## Installation

```bash
# Clone the repository
git clone <repository-url>

cd utils/nightly-quantum-entanglement-simulator

# Build
cargo build --release

# Run tests
cargo test
```

## License

MIT License - feel free to use for both classical and quantum computing projects!
