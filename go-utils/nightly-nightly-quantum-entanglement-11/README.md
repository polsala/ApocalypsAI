# Nightly Quantum Entanglement Checker

A whimsical-yet-useful utility that simulates quantum entanglement verification for distributed systems. Uses Go's concurrency primitives to demonstrate entanglement-like behavior between goroutines.

## Features

- Simulates quantum entanglement between distributed nodes
- Demonstrates Go's concurrency patterns (channels, goroutines, sync)
- Provides entanglement verification with spooky action at a distance
- Includes performance metrics and visualization
- Whimsical quantum-themed output

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd utils/nightly-quantum-entanglement-checker

# Build the utility
go build -o qec src/main.go

# Run the utility
./qec --nodes 5 --entanglement-factor 0.8
```

## Usage

```bash
# Basic usage with default settings
./qec

# Custom configuration
./qec --nodes 10 --entanglement-factor 0.9 --duration 30s

# Help
./qec --help
```

## Command Line Options

- `--nodes`: Number of quantum nodes to simulate (default: 5)
- `--entanglement-factor`: Probability of entanglement (0.0-1.0, default: 0.75)
- `--duration`: Simulation duration (default: 10s)
- `--verbose`: Enable detailed output

## Example Output

```
🔮 Initializing Quantum Entanglement Checker...

📍 Creating 5 quantum nodes...
⚛️  Node 1: Spinning up quantum state...
⚛️  Node 2: Spinning up quantum state...
⚛️  Node 3: Spinning up quantum state...
⚛️  Node 4: Spinning up quantum state...
⚛️  Node 5: Spinning up quantum state...

🔗 Establishing quantum entanglement...
✨ Node 1 entangled with Node 3 (spooky action!)
✨ Node 2 entangled with Node 4 (spooky action!)
✨ Node 5 remains independent (quantum solitude)

⏱️  Running entanglement verification for 10s...

📊 Entanglement Metrics:
   - Total nodes: 5
   - Entangled pairs: 2
   - Independent nodes: 1
   - Entanglement factor: 0.75
   - Quantum coherence: 94.2%
   - Spooky action detected: 100%

🎉 Quantum verification complete!
```

## Technical Details

This utility demonstrates:

- **Goroutines**: Each quantum node runs as an independent goroutine
- **Channels**: Quantum states are communicated via buffered channels
- **Sync primitives**: WaitGroups and Mutexes ensure thread-safe operations
- **Random quantum behavior**: Probabilistic entanglement simulation
- **Performance monitoring**: Real-time metrics collection

## Educational Value

- Learn Go's concurrency patterns through quantum metaphors
- Understand channel-based communication
- See practical examples of sync primitives
- Explore probabilistic algorithms

## License

MIT License - feel free to use in your quantum computing projects!

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add quantum improvements
4. Submit a pull request

May your code be as entangled as your quantum states! 🌌
