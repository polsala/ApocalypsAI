# Nightly Quantum Entanglement Checker

A whimsical-yet-useful CLI tool for detecting quantum entanglement patterns in quantum computing simulations. Perfect for quantum researchers, students, and curious minds!

## Features
- Detects Bell states and GHZ states
- Calculates entanglement entropy
- Validates quantum state normalization
- Generates random entangled states for testing
- High-performance Rust implementation

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd nightly-quantum-entanglement-checker

# Build with Cargo
cargo build --release

# Run the CLI
cargo run --release -- --help
```

## Usage

### Check if a quantum state is entangled
```bash
cargo run --release -- check --amplitudes 0.7071 0 0 0.7071
```

### Generate a random entangled state
```bash
cargo run --release -- generate --qubits 3
```

### Calculate entanglement entropy
```bash
cargo run --release -- entropy --amplitudes 0.5 0.5 0.5 0.5
```

## Examples

### Bell State Detection
```bash
# |Φ+⟩ = (|00⟩ + |11⟩) / √2
cargo run --release -- check --amplitudes 0.7071 0 0 0.7071
# Output: Entangled! This is a Bell state.
```

### GHZ State Detection
```bash
# |GHZ⟩ = (|000⟩ + |111⟩) / √2
cargo run --release -- check --amplitudes 0.7071 0 0 0 0 0 0 0.7071
# Output: Entangled! This is a GHZ state.
```

### Separable State
```bash
# |0⟩ ⊗ |1⟩ = |01⟩
cargo run --release -- check --amplitudes 0 1 0 0
# Output: Not entangled. This is a separable state.
```

## State Format

Amplitudes should be provided as real numbers representing the probability amplitudes of the quantum state in the computational basis.

For n qubits, provide 2^n amplitudes in the order:
|00...0⟩, |00...1⟩, |01...0⟩, ..., |11...1⟩

## Mathematical Background

- **Normalization**: ∑|α_i|² = 1
- **Entanglement Entropy**: S = -Tr(ρ_A log ρ_A)
- **Bell States**: Maximally entangled two-qubit states
- **GHZ States**: Maximally entangled multi-qubit states

## Performance

This tool is built in Rust for maximum performance when dealing with large quantum states. It can handle states with up to 10+ qubits efficiently.

## License

MIT License
