# Nightly Quantum Entanglement Simulator

A whimsical quantum entanglement simulator that demonstrates spooky action at a distance with ASCII visualization. Perfect for understanding quantum mechanics concepts or just watching particles dance!

## Features

- Simulates quantum entanglement between particle pairs
- ASCII visualization of particle states and measurements
- Configurable measurement bases and entanglement strength
- Spooky action at a distance demonstrations
- Educational tool for quantum mechanics concepts

## Installation

```bash
# Clone the repository
git clone <repository-url>

cd nightly-quantum-entanglement-simulator

# Build the project
cargo build --release
```

## Usage

```bash
# Run with default settings
./target/release/nightly-quantum-entanglement-simulator

# Run with custom configuration
./target/release/nightly-quantum-entanglement-simulator --particles 10 --measurements 5 --entanglement 0.8

# Run in verbose mode to see detailed measurements
./target/release/nightly-quantum-entanglement-simulator --verbose
```

## Command Line Options

- `--particles N`: Number of entangled particle pairs to simulate (default: 5)
- `--measurements N`: Number of measurements to perform (default: 3)
- `--entanglement N`: Entanglement strength (0.0 to 1.0, default: 0.9)
- `--verbose`: Show detailed measurement information
- `--help`: Show help message

## Example Output

```
=== Quantum Entanglement Simulation ===

Particle Pair 1:
  Alice: |0⟩ + |1⟩
  Bob:   |0⟩ + |1⟩
  Entanglement: ██████████ (100%)

Measurement 1:
  Alice measures in X basis: |+⟩
  Bob measures in X basis:  |+⟩
  Correlation: ✓ Perfect (spooky action!)

Measurement 2:
  Alice measures in Z basis: |0⟩
  Bob measures in Z basis:  |0⟩
  Correlation: ✓ Perfect (spooky action!)

Measurement 3:
  Alice measures in Y basis: |i⟩
  Bob measures in Y basis:  |-i⟩
  Correlation: ✓ Perfect (spooky action!)

=== Simulation Complete ===
```

## Educational Value

This simulator demonstrates key quantum mechanics concepts:

- **Superposition**: Particles exist in multiple states simultaneously
- **Entanglement**: Particles become correlated regardless of distance
- **Measurement**: Observing a particle collapses its state
- **Non-locality**: Changes to one particle instantly affect its partner

## License

MIT License - see LICENSE file for details.
