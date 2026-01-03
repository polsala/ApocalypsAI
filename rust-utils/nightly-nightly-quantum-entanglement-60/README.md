# Nightly Quantum Entanglement Simulator

A whimsical quantum entanglement simulator that generates entangled particle pairs and visualizes their spooky action at a distance.

## Features

- Generate entangled particle pairs with correlated properties
- Simulate measurement collapse across arbitrary distances
- Visualize quantum states with ASCII art
- Calculate Bell inequality violations
- Export results to JSON for analysis

## Usage

```bash
# Build the simulator
$ cargo build --release

# Run with default settings (100 particle pairs)
$ ./target/release/nightly-quantum-entanglement-simulator

# Run with custom settings
$ ./target/release/nightly-quantum-entanglement-simulator --pairs 1000 --distance 1000000

# Export results to JSON
$ ./target/release/nightly-quantum-entanglement-simulator --export results.json
```

## Output

The simulator displays:
- Entangled particle pairs with their properties
- Measurement results showing perfect correlation
- Bell inequality calculation
- "Spooky action at a distance" visualization

## Example Output

```
=== QUANTUM ENTANGLEMENT SIMULATION ===

Generating 100 entangled particle pairs...

Particle Pair #1:
  Alice measures: Spin Up (+1) at angle 45°
  Bob measures:   Spin Down (-1) at angle 45°
  Distance: 1000 km
  Result: Perfect anti-correlation ✓

Particle Pair #2:
  Alice measures: Spin Down (-1) at angle 120°
  Bob measures:   Spin Up (+1) at angle 120°
  Distance: 1000 km
  Result: Perfect anti-correlation ✓

...

BELL INEQUALITY TEST:
  Measured correlation: -0.707
  Classical limit:      -0.500
  Quantum violation:    ✓ (29.3%)

"Spooky action at a distance" confirmed! 🎃👻
```

## Installation

Requires Rust 1.70+:

```bash
$ git clone <repository>
$ cd nightly-quantum-entanglement-simulator
$ cargo build --release
```

## License

MIT - because quantum physics should be fun for everyone!
