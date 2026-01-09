# Nightly Quantum Entanglement Simulator

A whimsical Go-based utility that simulates quantum entanglement for distributed systems, providing fun quantum state visualization and entanglement verification for developers.

## Features

- 🎭 **Quantum State Simulation**: Simulate quantum states with superposition and entanglement
- 📊 **Real-time Visualization**: ASCII art visualization of quantum states and entanglement
- 🔗 **Entanglement Verification**: Verify quantum entanglement between simulated particles
- 🎮 **Interactive Mode**: Command-line interface for exploring quantum phenomena
- 📈 **Performance Metrics**: Track quantum operations and entanglement efficiency

## Installation

```bash
# Clone the repository
git clone <repository-url>

# Navigate to the utility
cd utils/nightly-quantum-entanglement-simulator

# Build the utility
go build -o qsim ./src

# Run the simulator
./qsim --help
```

## Usage

### Basic Simulation
```bash
# Simulate quantum entanglement between 2 particles
./qsim simulate --particles 2 --duration 10s

# Visualize quantum states
./qsim visualize --particles 3

# Verify entanglement
./qsim verify --particles 2 --entanglement-factor 0.8
```

### Advanced Options
```bash
# Custom quantum operations
./qsim simulate --particles 4 --operations hadamard,cnot,measure

# Performance analysis
./qsim analyze --particles 8 --iterations 1000

# Interactive mode
./qsim interactive
```

## Examples

### Quantum Coin Flip
```bash
./qsim simulate --particles 1 --operations hadamard,measure --visualize
```

### Bell State Creation
```bash
./qsim simulate --particles 2 --operations hadamard,cnot --entangled
```

### Quantum Random Number Generator
```bash
./qsim simulate --particles 8 --operations hadamard,measure --output-format binary
```

## Quantum Operations

- **Hadamard**: Creates superposition
- **CNOT**: Creates entanglement
- **Measure**: Collapses quantum state
- **Phase**: Applies phase shift
- **Swap**: Exchanges quantum states

## Output Formats

- **ASCII**: Visual representation of quantum states
- **Binary**: Binary output for quantum random numbers
- **JSON**: Structured data for programmatic use
- **Text**: Human-readable quantum state description

## Performance

The simulator is optimized for educational and entertainment purposes:

- **Particle Limit**: Up to 16 simulated particles
- **Operation Speed**: ~1 million operations per second
- **Memory Usage**: ~1MB per 8 particles
- **Visualization**: Real-time ASCII art updates

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Add tests for new quantum operations
2. Update documentation for new features
3. Maintain backward compatibility
4. Follow Go best practices

## Disclaimer

This is a simulation for entertainment and educational purposes only. It does not represent actual quantum computing capabilities.

## Quantum Computing Resources

- [IBM Quantum Experience](https://quantum-computing.ibm.com/)
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Microsoft Quantum Development Kit](https://docs.microsoft.com/quantum/)
- [Google Cirq Framework](https://quantumai.google/cirq)
