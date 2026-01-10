# Nightly Quantum Entanglement Simulator

A whimsical CLI tool that simulates quantum entanglement states for fun and education. Perfect for understanding quantum mechanics concepts in a playful way!

## Features

- Simulate quantum entanglement between particles
- Visualize quantum states with ASCII art
- Generate random quantum measurements
- Educational explanations of quantum phenomena
- Whimsical particle names and descriptions

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd utils/nightly-quantum-entanglement-simulator

# Build the project
cargo build --release

# Run the simulator
cargo run --release
```

## Usage

```bash
# Basic simulation
./target/release/nightly-quantum-entanglement-simulator

# Simulate with custom particle count
./target/release/nightly-quantum-entanglement-simulator --particles 5

# Enable verbose output
./target/release/nightly-quantum-entanglement-simulator --verbose

# Generate quantum measurement
./target/release/nightly-quantum-entanglement-simulator measure
```

## Examples

### Basic Entanglement Simulation

```bash
$ ./target/release/nightly-quantum-entanglement-simulator

=== QUANTUM ENTANGLEMENT SIMULATION ===

Particle 1 (Schrödinger's Sparkle): |↑⟩
Particle 2 (Heisenberg's Hilarity): |↓⟩

Entanglement Status: ✨ QUANTUMLY CONNECTED ✨

Measurement Result: Both particles collapsed to opposite states!

Explanation: When entangled particles are measured, they always show correlated results,
even when separated by vast distances. Spooky action at a distance!
```

### Quantum Measurement

```bash
$ ./target/release/nightly-quantum-entanglement-simulator measure

=== QUANTUM MEASUREMENT ===

Random Particle State: |ψ⟩ = 0.707|↑⟩ + 0.707|↓⟩
Measurement Outcome: |↑⟩ (Spin Up)

Probability of this outcome: 50.00%

Fun Fact: Before measurement, the particle exists in a superposition of both states!
```

## Educational Concepts

This simulator demonstrates several key quantum mechanics concepts:

1. **Superposition**: Particles can exist in multiple states simultaneously
2. **Entanglement**: Particles can be linked such that measuring one instantly affects the other
3. **Wave Function Collapse**: Measurement forces a particle into a definite state
4. **Quantum Correlation**: Entangled particles show perfectly correlated measurement results

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This is a whimsical educational tool and not a scientifically accurate quantum simulator. It's designed to introduce concepts in a fun way, not to replace proper quantum mechanics education.
