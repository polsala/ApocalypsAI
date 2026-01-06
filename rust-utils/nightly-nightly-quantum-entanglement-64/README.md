# Nightly Quantum Entanglement Simulator

A whimsical quantum circuit simulator written in Rust that visualizes quantum states and detects entanglement patterns. Perfect for learning quantum computing concepts or just watching spooky action at a distance!

## Features

- 🎯 **Quantum Circuit Simulation**: Simulate qubits, gates, and measurements
- 🎨 **ASCII Visualization**: Beautiful text-based circuit diagrams
- 🌀 **Entanglement Detection**: Automatically identifies entangled qubit pairs
- 🎲 **Probabilistic Outcomes**: Shows measurement probabilities
- 🚀 **High Performance**: Rust-powered for lightning-fast simulation

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd utils/nightly-quantum-entanglement-simulator

# Build the project
cargo build --release
```

## Usage

### Basic Circuit Simulation

```bash
# Run the simulator
cargo run --release

# Or with specific examples
cargo run --release -- --example bell_state
cargo run --release -- --example ghz_state
cargo run --release -- --example random_circuit
```

### Command Line Options

```bash
--help              Show help message
--example <NAME>   Run predefined example (bell_state, ghz_state, random_circuit)
--qubits <N>        Number of qubits (default: 2)
--depth <N>         Circuit depth (default: 3)
--seed <N>          Random seed for reproducible circuits
```

### Programmatic Usage

```rust
use nightly_quantum_entanglement_simulator::*;

// Create a 2-qubit system
let mut circuit = QuantumCircuit::new(2);

// Add gates
let h_gate = Gate::Hadamard(0);
let cnot_gate = Gate::CNOT(0, 1);

circuit.add_gate(h_gate);
circuit.add_gate(cnot_gate);

// Simulate and measure
let result = circuit.simulate();
println!("{}", result);

// Check for entanglement
if circuit.is_entangled() {
    println!("🎉 Entanglement detected!");
}
```

## Examples

### Bell State (Maximally Entangled)

```
Qubit 0: |0⟩ ── H ──●── Measurement
                    |
Qubit 1: |0⟩ ─────── X ── Measurement

Entanglement detected between qubits 0 and 1!
Measurement results: 50% |00⟩, 50% |11⟩
```

### GHZ State (Multi-qubit Entanglement)

```
Qubit 0: |0⟩ ── H ──●──●── Measurement
                    |  |
Qubit 1: |0⟩ ─────── X  |── Measurement
                       |
Qubit 2: |0⟩ ────────── X ── Measurement

Entanglement detected between qubits 0, 1, and 2!
Measurement results: 50% |000⟩, 50% |111⟩
```

## Quantum Gates Supported

- **Hadamard (H)**: Creates superposition
- **Pauli-X (X)**: Bit flip (NOT gate)
- **Pauli-Y (Y)**: Phase and bit flip
- **Pauli-Z (Z)**: Phase flip
- **CNOT**: Controlled NOT (entanglement gate)
- **CZ**: Controlled Z (phase entanglement)
- **SWAP**: Swaps qubit states
- **Toffoli**: Controlled-controlled NOT

## Entanglement Detection

The simulator uses the **concurrence measure** to detect entanglement:

- **Concurrence = 0**: No entanglement (separable state)
- **Concurrence = 1**: Maximally entangled
- **0 < Concurrence < 1**: Partially entangled

## Performance

- **Simulation Speed**: ~1M operations/second on modern hardware
- **Memory Usage**: O(2^n) for n qubits (standard for state vector simulation)
- **Entanglement Detection**: O(n²) for n qubits

## Testing

```bash
# Run all tests
cargo test

# Run with coverage
cargo tarpaulin --out Html

# Run specific test
cargo test test_bell_state_entanglement
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Quantum Computing Resources

- [Qiskit Textbook](https://qiskit.org/textbook)
- [Quantum Country](https://quantum.country)
- [Microsoft Quantum Development Kit](https://docs.microsoft.com/quantum/)

## Disclaimer

This simulator is for educational and entertainment purposes. It uses simplified quantum mechanics models and should not be used for actual quantum computing research or production systems.

---

*"Spooky action at a distance" - Albert Einstein*
