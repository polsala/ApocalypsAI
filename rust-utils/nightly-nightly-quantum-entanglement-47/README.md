# Nightly Quantum Entanglement Simulator

A whimsical quantum entanglement simulator that generates entangled particle pairs and visualizes their spooky action at a distance. Perfect for understanding quantum mechanics concepts or just watching particles dance across dimensions!

## Features

- Generate entangled particle pairs with random quantum states
- Visualize quantum state collapse when one particle is observed
- Simulate quantum teleportation protocols
- Display spooky action at a distance effects
- Export simulation results to JSON

## Usage

```bash
# Run the simulator
./nightly-quantum-entanglement-simulator

# Generate 10 entangled pairs
./nightly-quantum-entanglement-simulator --pairs 10

# Export results to file
./nightly-quantum-entanglement-simulator --export results.json

# Run in verbose mode
./nightly-quantum-entanglement-simulator --verbose
```

## Quantum States

The simulator supports:
- **Spin states**: Up (↑) and Down (↓)
- **Polarization**: Horizontal (↔) and Vertical (↕)
- **Color states**: Red, Green, Blue
- **Position states**: Localized in different dimensions

## Spooky Action

When one particle of an entangled pair is observed, its partner instantly collapses to the opposite state, regardless of distance. This demonstrates the famous "spooky action at a distance" that Einstein found so puzzling.

## Installation

```bash
# Clone the repository
git clone <repo-url>

# Navigate to the utility
cd utils/rust-utils/nightly-quantum-entanglement-simulator

# Build the project
cargo build --release

# Run the simulator
./target/release/nightly-quantum-entanglement-simulator
```

## License

MIT License - feel free to use for educational purposes!
