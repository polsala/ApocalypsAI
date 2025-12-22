# Nightly Quantum Entanglement Checker

A whimsical-yet-useful Rust CLI tool that simulates quantum entanglement verification for distributed systems using Bell state measurements. Perfect for testing distributed consensus algorithms and understanding quantum-inspired computing concepts.

## Features

- Simulates Bell state measurements for quantum entanglement verification
- Generates random quantum states and measures entanglement fidelity
- Provides statistical analysis of entanglement over multiple trials
- Supports both local simulation and distributed mode
- Includes educational output explaining quantum mechanics concepts

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd utils/nightly-quantum-entanglement-checker

# Build the project
cargo build --release

# Run the tool
cargo run --release -- --help
```

## Usage

### Basic Entanglement Check
```bash
# Check entanglement between two simulated qubits
cargo run --release -- check-entanglement --qubits 2 --trials 1000
```

### Distributed Mode
```bash
# Simulate entanglement across distributed nodes
cargo run --release -- distributed --nodes 4 --trials 500
```

### Bell State Analysis
```bash
# Analyze Bell state measurements
cargo run --release -- bell-state --state phi-plus --measurements 100
```

### Help
```bash
cargo run --release -- --help
```

## Examples

### Example 1: Basic Entanglement Verification
```bash
cargo run --release -- check-entanglement --qubits 2 --trials 1000
```

Output:
```
Quantum Entanglement Verification Results:
----------------------------------------
Qubits: 2
Trials: 1000
Entanglement Fidelity: 0.987
Bell Inequality Violation: 2.71

Interpretation: Strong entanglement detected!
Classical limit: 2.0, Quantum result: 2.71
```

### Example 2: Distributed System Simulation
```bash
cargo run --release -- distributed --nodes 4 --trials 500
```

Output:
```
Distributed Entanglement Simulation:
-----------------------------------
Nodes: 4
Trials per node: 500
Global entanglement fidelity: 0.945
Network synchronization: 98.2%

Node 1: Fidelity 0.942
Node 2: Fidelity 0.948
Node 3: Fidelity 0.941
Node 4: Fidelity 0.949
```

## Quantum Mechanics Concepts

This tool demonstrates several key quantum mechanics principles:

- **Superposition**: Qubits can exist in multiple states simultaneously
- **Entanglement**: Particles become correlated such that measurement of one instantly affects the other
- **Bell States**: Maximally entangled quantum states of two qubits
- **Bell Inequality**: Mathematical limit that distinguishes classical from quantum correlations

## Educational Use

This tool is perfect for:
- Computer science courses on quantum computing
- Physics demonstrations of quantum phenomena
- Research into quantum-inspired algorithms
- Understanding the fundamentals of quantum entanglement

## Technical Details

- Uses Rust's `rand` crate for quantum state generation
- Implements Bell state measurements using Pauli matrices
- Calculates CHSH inequality for entanglement verification
- Provides statistical confidence intervals for results

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please follow standard Rust conventions and include tests for new features.

## Disclaimer

This tool simulates quantum mechanics concepts for educational and testing purposes. It does not perform actual quantum computations.
