# Nightly Quantum Entanglement Simulator

A whimsical Go-based CLI tool that simulates quantum entanglement for fun and educational purposes. Perfect for understanding quantum mechanics concepts in an interactive way!

## Features

- Simulate quantum entanglement between particles
- Visualize entanglement states with ASCII art
- Educational explanations of quantum concepts
- Random quantum state generation
- Measurement simulation with probabilistic outcomes

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd utils/nightly-quantum-entanglement-simulator

# Build the binary
go build -o quantum-simulator ./src

# Run the simulator
./quantum-simulator
```

## Usage

```bash
# Basic simulation
./quantum-simulator

# Simulate with custom particle count
./quantum-simulator --particles 5

# Run with verbose output
./quantum-simulator --verbose

# Generate quantum state explanation
./quantum-simulator --explain
```

## Examples

### Basic Entanglement Simulation

```
$ ./quantum-simulator

=== Quantum Entanglement Simulation ===

Particle A: |0⟩
Particle B: |1⟩

Entanglement Status: ✓ ENTANGLED
Measurement Correlation: Perfect Anti-Correlation

When Particle A is measured as 0, Particle B will be 1!
```

### Multi-Particle System

```
$ ./quantum-simulator --particles 3

=== Multi-Particle Quantum System ===

Particle 1: |+⟩ (Superposition)
Particle 2: |-⟩ (Superposition)
Particle 3: |0⟩ (Collapsed)

Entanglement Network:
1 ↔ 2: ✓ Entangled
1 ↔ 3: ✗ Not Entangled
2 ↔ 3: ✗ Not Entangled
```

## Quantum Concepts Explained

### Superposition
A quantum particle can exist in multiple states simultaneously until measured.

### Entanglement
When particles become entangled, the state of one instantly affects the other, regardless of distance.

### Measurement
Measuring a quantum system causes it to collapse from superposition to a definite state.

## Educational Value

This simulator helps understand:
- Quantum superposition principles
- Entanglement phenomena
- Measurement effects
- Quantum state visualization

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - see LICENSE file for details.

## Disclaimer

This is a simplified educational tool and does not represent actual quantum physics with complete accuracy. It's designed for fun and learning purposes.
