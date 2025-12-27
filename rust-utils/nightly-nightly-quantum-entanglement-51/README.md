# Nightly Quantum Entanglement Simulator

A whimsical CLI tool that simulates quantum entanglement states for fun and educational purposes. Perfect for understanding quantum mechanics concepts in a playful way!

## Features

- Simulate quantum entanglement between particles
- Visualize quantum states with ASCII art
- Generate random quantum measurements
- Educational mode with explanations
- Save/load quantum states to files

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd utils/nightly-quantum-entanglement-simulator

# Build the project
cargo build --release

# Run the simulator
./target/release/nightly-quantum-entanglement-simulator
```

## Usage

```bash
# Basic simulation
./target/release/nightly-quantum-entanglement-simulator --particles 2 --measurements 5

# Educational mode with explanations
./target/release/nightly-quantum-entanglement-simulator --educational --particles 3

# Save quantum state to file
./target/release/nightly-quantum-entanglement-simulator --save state.json

# Load quantum state from file
./target/release/nightly-quantum-entanglement-simulator --load state.json

# Help
./target/release/nightly-quantum-entanglement-simulator --help
```

## Examples

### Basic Entanglement Simulation

```bash
$ ./target/release/nightly-quantum-entanglement-simulator --particles 2 --measurements 3

=== Quantum Entanglement Simulation ===
Particles: 2
Measurements: 3

Initial State: |00⟩
Entanglement Applied: Bell State Created

Measurement 1:
Particle 1: ↑ (spin up)
Particle 2: ↓ (spin down)
Correlation: Perfect anti-correlation ✓

Measurement 2:
Particle 1: ↓ (spin down)
Particle 2: ↑ (spin up)
Correlation: Perfect anti-correlation ✓

Measurement 3:
Particle 1: ↑ (spin up)
Particle 2: ↓ (spin down)
Correlation: Perfect anti-correlation ✓

=== Simulation Complete ===
```

### Educational Mode

```bash
$ ./target/release/nightly-quantum-entanglement-simulator --educational --particles 2

=== Quantum Entanglement Simulation (Educational Mode) ===

What is Quantum Entanglement?
Quantum entanglement is a physical phenomenon that occurs when pairs or groups of particles are generated, interact, or share spatial proximity in ways such that the quantum state of each particle cannot be described independently of the state of the others.

Initial State: |00⟩
This represents two particles both in the '0' state (spin down).

Applying Hadamard Gate to Particle 1...
This creates a superposition of states: (|0⟩ + |1⟩)/√2

Applying CNOT Gate...
This entangles the particles, creating a Bell state: (|00⟩ + |11⟩)/√2

Now the particles are entangled! Measuring one instantly determines the state of the other, no matter how far apart they are.

Measurement 1:
Particle 1: ↑ (spin up)
Particle 2: ↑ (spin up)
Explanation: Due to entanglement, both particles collapsed to the same state!

=== Educational Simulation Complete ===
```

## Quantum States Visualization

The simulator includes ASCII art visualizations of quantum states:

```
Particle States:
┌─────────┐ ┌─────────┐
│ Particle│ │ Particle│
│    1    │ │    2    │
│  ↑ ↓    │ │  ↑ ↓    │
│  ● ○    │ │  ○ ●    │
└─────────┘ └─────────┘
```

## Quantum Concepts Explained

### Superposition
A quantum system can exist in multiple states simultaneously until measured.

### Entanglement
When particles become entangled, the state of one instantly influences the state of the other, regardless of distance.

### Measurement Collapse
When a quantum system is measured, it 'collapses' from superposition to a definite state.

### Bell States
Special entangled states that exhibit perfect correlations between particles.

## File Format

Quantum states are saved in JSON format:

```json
{
  "particles": 2,
  "state": "bell",
  "coefficients": [0.707, 0.707],
  "measurements": [
    {"particle_1": "up", "particle_2": "down"},
    {"particle_1": "down", "particle_2": "up"}
  ]
}
```

## Dependencies

- Rust 1.70+
- Standard library only (no external dependencies)

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Disclaimer

This is a simplified educational tool and does not represent actual quantum computing. It's designed to help understand basic quantum concepts in a fun way!

## Fun Facts

- Einstein called entanglement "spooky action at a distance"
- Quantum entanglement is used in real quantum computing and quantum cryptography
- The simulator uses classical computation to model quantum behavior
- No actual quantum particles were harmed in the making of this tool!
