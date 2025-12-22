# Nightly Quantum Entanglement Simulator

A whimsical quantum circuit simulator that visualizes quantum states and entanglement with ASCII art. Perfect for learning quantum computing concepts!

## Features

- Simulate quantum circuits with qubits and gates
- Visualize quantum states with ASCII art
- Demonstrate quantum entanglement
- Educational tool for quantum computing concepts
- Command-line interface with interactive mode

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd nightly-quantum-entanglement-simulator

# Build with Cargo
cargo build --release
```

## Usage

### Basic Circuit Simulation

```bash
# Simulate a simple Bell state circuit
cargo run --release -- --qubits 2 --gates h(0) cx(0,1)
```

### Interactive Mode

```bash
# Start interactive mode
cargo run --release -- --interactive
```

### Load Circuit from File

```bash
# Load circuit definition from JSON file
cargo run --release -- --file circuit.json
```

## Circuit Definition Format

Circuits can be defined using:

- `h(qubit)` - Hadamard gate
- `x(qubit)` - Pauli-X gate
- `y(qubit)` - Pauli-Y gate
- `z(qubit)` - Pauli-Z gate
- `cx(control,target)` - CNOT gate
- `cz(control,target)` - Controlled-Z gate
- `swap(qubit1,qubit2)` - SWAP gate

Example:
```
--qubits 3 --gates h(0) cx(0,1) cx(1,2)
```

## Output

The simulator displays:

1. **Circuit Diagram**: ASCII visualization of the quantum circuit
2. **State Vector**: Probability amplitudes of all basis states
3. **Measurement Probabilities**: Likelihood of each measurement outcome
4. **Entanglement Analysis**: Detection of entangled qubits

## Examples

### Bell State
```bash
cargo run --release -- --qubits 2 --gates h(0) cx(0,1)
```

### GHZ State
```bash
cargo run --release -- --qubits 3 --gates h(0) cx(0,1) cx(1,2)
```

### Quantum Teleportation
```bash
cargo run --release -- --qubits 3 --gates h(1) cx(1,2) cx(0,1) h(0) cx(1,2) cz(0,2)
```

## Educational Value

This simulator helps understand:

- Quantum superposition
- Quantum entanglement
- Quantum gates and operations
- Measurement in quantum mechanics
- Multi-qubit systems

## Dependencies

- Rust 1.70+
- Standard library only (no external dependencies)

## License

MIT License - see LICENSE file for details.
