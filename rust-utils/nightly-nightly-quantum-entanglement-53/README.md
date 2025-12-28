# Nightly Quantum Entanglement Simulator

A whimsical quantum entanglement simulator that demonstrates spooky action at a distance with ASCII visualization. Perfect for understanding quantum mechanics concepts or just watching particles dance!

## Features

- Simulates quantum entanglement between particle pairs
- ASCII visualization of particle states and measurements
- Configurable entanglement strength and measurement probability
- Educational tool for quantum mechanics concepts
- Cross-platform Rust binary

## Installation

### From Source

```bash
# Clone the repository
# cd to the quantum-entanglement-simulator directory

# Build the project
cargo build --release

# Run the simulator
cargo run --release
```

### Pre-built Binary

Download the latest release for your platform from the releases page.

## Usage

```bash
# Run with default settings
cargo run --release

# Run with custom configuration
cargo run --release -- --entanglement-strength 0.8 --measurement-probability 0.3

# Show help
cargo run --release -- --help
```

## Configuration Options

- `--entanglement-strength`: Strength of entanglement (0.0 to 1.0, default: 0.7)
- `--measurement-probability`: Probability of measuring a particle (0.0 to 1.0, default: 0.5)
- `--duration`: Simulation duration in seconds (default: 10)
- `--particles`: Number of entangled pairs (default: 5)

## Example Output

```
Quantum Entanglement Simulation Starting...

Particle Pair 1: [↑] ⟷ [↓]  (Entangled)
Particle Pair 2: [↓] ⟷ [↑]  (Entangled)
Particle Pair 3: [↑] ⟷ [↓]  (Entangled)

Measurement Event! Particle 1A collapsed to: ↑
Spooky action! Particle 1B instantly became: ↓

Particle Pair 1: [↑] ⟷ [↓]  (Measured)
Particle Pair 2: [↓] ⟷ [↑]  (Entangled)
Particle Pair 3: [↑] ⟷ [↓]  (Entangled)
```

## Educational Value

This simulator demonstrates key quantum mechanics concepts:

- **Superposition**: Particles exist in multiple states until measured
- **Entanglement**: Particles become linked, affecting each other instantly
- **Measurement Collapse**: Observing a particle forces it into a definite state
- **Non-locality**: Entangled particles affect each other regardless of distance

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please follow standard Rust conventions and include tests for new features.

## Disclaimer

This is a simplified educational tool and does not represent actual quantum physics with complete accuracy. Real quantum mechanics is much more complex!
