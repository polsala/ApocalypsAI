# Nightly Quantum Entanglement Simulator

A whimsical CLI tool that simulates quantum entanglement states for fun and educational purposes. Perfect for understanding quantum mechanics concepts in an interactive way!

## Features

- Simulate quantum entanglement between particles
- Visualize quantum states with ASCII art
- Generate random quantum measurements
- Educational mode with explanations
- Save and load quantum state configurations

## Installation

### From Source (Rust)

```bash
# Clone the repository
# Navigate to the rust-utils/nightly-quantum-entanglement-simulator directory

# Build the project
cargo build --release

# Run the simulator
./target/release/nightly-quantum-entanglement-simulator
```

### Prerequisites

- Rust 1.70+ installed
- Terminal that supports UTF-8 characters

## Usage

```bash
# Basic simulation
./target/release/nightly-quantum-entanglement-simulator simulate

# Educational mode with explanations
./target/release/nightly-quantum-entanglement-simulator educate

# Generate random measurements
./target/release/nightly-quantum-entanglement-simulator measure

# Save current state
./target/release/nightly-quantum-entanglement-simulator save --file my_state.json

# Load saved state
./target/release/nightly-quantum-entanglement-simulator load --file my_state.json

# View help
./target/release/nightly-quantum-entanglement-simulator --help
```

## Examples

### Basic Simulation

```bash
$ ./target/release/nightly-quantum-entanglement-simulator simulate

=== Quantum Entanglement Simulation ===
Particle A: |↑⟩
Particle B: |↓⟩
Entanglement: ✓ Active
Correlation: Perfect anti-correlation

Measurement Result:
Particle A collapses to: ↑ (spin up)
Particle B collapses to: ↓ (spin down)
```

### Educational Mode

```bash
$ ./target/release/nightly-quantum-entanglement-simulator educate

=== Quantum Entanglement Explained ===

What is Quantum Entanglement?
Quantum entanglement is a physical phenomenon that occurs when pairs or groups of particles are generated, interact, or share spatial proximity in ways such that the quantum state of each particle cannot be described independently of the state of the others.

Key Concepts:
• Superposition: Particles can exist in multiple states simultaneously
• Measurement: Observing a particle forces it into a definite state
• Non-locality: Entangled particles affect each other instantaneously, regardless of distance

Simulation:
Particle A: |↑⟩ + |↓⟩ (superposition)
Particle B: |↑⟩ + |↓⟩ (superposition)
Entanglement: ✓ Active

When we measure Particle A and find it in state |↑⟩, Particle B instantly becomes |↓⟩!
```

## Command Reference

### simulate
Run a quantum entanglement simulation.

**Options:**
- `--particles N`: Number of entangled particles (default: 2)
- `--iterations N`: Number of simulation iterations (default: 1)

### educate
Display educational content about quantum entanglement.

**Options:**
- `--topic TOPIC`: Specific topic to explain (superposition, measurement, nonlocality)

### measure
Generate random quantum measurements.

**Options:**
- `--basis BASIS`: Measurement basis (z, x, y)
- `--count N`: Number of measurements to generate (default: 10)

### save
Save the current quantum state to a file.

**Options:**
- `--file FILE`: Output file path (default: quantum_state.json)

### load
Load a quantum state from a file.

**Options:**
- `--file FILE`: Input file path (default: quantum_state.json)

## Quantum States

The simulator supports various quantum states:

- **|↑⟩**: Spin up
- **|↓⟩**: Spin down
- **|→⟩**: Right polarization
- **|←⟩**: Left polarization
- **|↗⟩**: Diagonal polarization
- **|↖⟩**: Anti-diagonal polarization

## ASCII Art Visualizations

The simulator includes beautiful ASCII art representations of quantum states:

```
Particle A:  /\    (spin up)
             ||

Particle B:  ||    (spin down)
             \/
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is a whimsical educational tool and not a scientifically accurate quantum simulator. It's designed to introduce concepts in an accessible way.

## Quantum Joke of the Day

Why don't quantum physicists ever get lost?

Because they always know their position... and their momentum... but never both at the same time! 🤪

---

*Made with ❤️ by the ApocalypsAI community*
