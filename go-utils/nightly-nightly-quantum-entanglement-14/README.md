# Nightly Quantum Entanglement Checker

A whimsical-yet-useful utility that simulates quantum entanglement verification for distributed systems. Perfect for testing concurrent operations and demonstrating Go's powerful concurrency features!

## Features

- Simulates quantum particle entanglement across goroutines
- Demonstrates Go's channel-based communication patterns
- Provides whimsical quantum-themed output
- Includes comprehensive tests with deterministic behavior
- Self-contained with no external dependencies

## Usage

```bash
# Build the utility
go build -o nightly-quantum-entanglement-checker

# Run with default settings
./nightly-quantum-entanglement-checker

# Run with custom particle count
./nightly-quantum-entanglement-checker -particles 100

# Run in verbose mode
./nightly-quantum-entanglement-checker -verbose
```

## Example Output

```
🔬 Initializing quantum entanglement verification...

Particle 1 (spin: ↑) entangled with Particle 2 (spin: ↓)
Particle 3 (spin: ↓) entangled with Particle 4 (spin: ↑)
Particle 5 (spin: ↑) entangled with Particle 6 (spin: ↓)

✅ Quantum entanglement verification complete!
📊 Entangled pairs: 3
⚡ Total particles: 6
🔬 Measurement correlation: 100.00%
```

## Installation

This utility requires Go 1.20 or later.

```bash
go get github.com/polsala/ApocalypsAI/go-utils/nightly-quantum-entanglement-checker
```

## Testing

Run the comprehensive test suite:

```bash
go test -v ./...
```

## Technical Details

This utility demonstrates several Go concurrency patterns:

- **Goroutines**: Simulate independent quantum particles
- **Channels**: Coordinate entanglement verification
- **WaitGroups**: Ensure all particles are measured
- **Mutexes**: Protect shared state during measurement

The simulation is completely deterministic for testing purposes, using seeded random number generation.

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please ensure all new features include:

- Comprehensive tests
- Clear documentation
- Deterministic behavior for testing

## Disclaimer

This utility is for educational and entertainment purposes only. It does not perform actual quantum physics calculations or measurements. The "quantum" aspects are purely whimsical simulations.
