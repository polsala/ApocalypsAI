# Nightly Quantum Entanglement Simulator

A whimsical quantum circuit simulator written in Rust that visualizes quantum gates and detects entanglement with ASCII art. Perfect for understanding quantum computing concepts or just watching pretty quantum animations!

## Features

- 🎯 **Quantum Gate Simulation**: Apply Hadamard, Pauli-X, Pauli-Y, Pauli-Z, CNOT, and Phase gates
- 🌀 **Entanglement Detection**: Automatically detects when qubits become entangled
- 🎨 **ASCII Visualization**: Beautiful quantum state visualization with spin arrows and probability clouds
- 🧪 **Interactive Mode**: Build circuits step-by-step with real-time feedback
- 📊 **Measurement Simulation**: Simulate quantum measurement with probabilistic outcomes
- 🎭 **Whimsical Output**: Fun quantum-themed messages and ASCII art

## Installation

```bash
# Clone the repository
git clone <repository-url>

cd utils/nightly-quantum-entanglement-simulator

# Build the project
cargo build --release

# Run the simulator
./target/release/nightly-quantum-entanglement-simulator
```

## Usage

### Interactive Mode

```bash
./target/release/nightly-quantum-entanglement-simulator --interactive
```

This launches an interactive session where you can:
- Add quantum gates to your circuit
- View the current quantum state
- Measure qubits
- Reset the system
- Exit the session

### Command Line Mode

```bash
# Create a simple Bell state
./target/release/nightly-quantum-entanglement-simulator --circuit "H(0), CNOT(0,1)"

# Apply gates and measure
./target/release/nightly-quantum-entanglement-simulator --circuit "H(0), X(1), CNOT(0,1), measure(0), measure(1)"

# View help
./target/release/nightly-quantum-entanglement-simulator --help
```

## Circuit Syntax

The circuit syntax supports the following gates:

- `H(n)` - Hadamard gate on qubit n
- `X(n)` - Pauli-X (NOT) gate on qubit n
- `Y(n)` - Pauli-Y gate on qubit n
- `Z(n)` - Pauli-Z gate on qubit n
- `CNOT(c,t)` - CNOT gate with control c and target t
- `S(n)` - Phase (S) gate on qubit n
- `T(n)` - T gate on qubit n
- `measure(n)` - Measure qubit n

Multiple gates can be separated by commas.

## Examples

### Bell State Creation

```bash
./target/release/nightly-quantum-entanglement-simulator --circuit "H(0), CNOT(0,1)"
```

This creates a Bell state where qubits 0 and 1 are maximally entangled.

### GHZ State Creation

```bash
./target/release/nightly-quantum-entanglement-simulator --circuit "H(0), CNOT(0,1), CNOT(1,2)"
```

This creates a 3-qubit GHZ state with all qubits entangled.

### Quantum Teleportation Circuit

```bash
./target/release/nightly-quantum-entanglement-simulator --circuit "H(1), CNOT(1,2), CNOT(0,1), H(0), measure(0), measure(1), X(2), Z(2)"
```

## ASCII Visualization

The simulator displays quantum states using ASCII art:

```
Qubit 0: |↑⟩  (α = 0.707 + 0.000i, |α|² = 0.50)
Qubit 1: |↓⟩  (β = 0.000 + 0.707i, |β|² = 0.50)

Entanglement detected! Qubits 0 and 1 are quantumly entwined! 🌀

Probability Cloud:
  |00⟩: 0.00%  |01⟩: 50.00%  |10⟩: 50.00%  |11⟩: 0.00%
```

## Entanglement Detection

The simulator automatically detects when qubits become entangled by analyzing the quantum state vector. When entanglement is detected, it displays:

- Which qubits are entangled
- The entanglement strength
- A whimsical quantum-themed message

## Testing

Run the test suite:

```bash
cargo test
```

The tests cover:
- Basic gate operations
- Entanglement detection
- Measurement simulation
- Circuit parsing
- Edge cases and error handling

## Performance

The simulator is optimized for educational use with up to 10 qubits. For larger systems, consider using professional quantum simulators.

## Contributing

Contributions are welcome! Please:

1. Follow Rust best practices
2. Add tests for new functionality
3. Update documentation
4. Ensure all tests pass

## License

MIT License - see LICENSE file for details.

## Quantum Disclaimer

This simulator is for educational and entertainment purposes. It doesn't replace actual quantum hardware or professional simulation tools.

*"If you think you understand quantum mechanics, you don't understand quantum mechanics."* - Richard Feynman
