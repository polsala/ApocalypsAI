# Nightly Quantum Entanglement Checker

A whimsical-yet-useful Rust CLI tool that simulates quantum entanglement verification for distributed systems using Bell state measurements. Perfect for testing distributed consensus algorithms and understanding quantum computing concepts!

## Features

- Simulates Bell state measurements (|Φ⁺⟩, |Φ⁻⟩, |Ψ⁺⟩, |Ψ⁻⟩)
- Generates entanglement verification reports
- Supports multiple measurement bases (computational, Hadamard)
- Calculates quantum fidelity and concurrence
- Export results to JSON, YAML, or plain text

## Installation

```bash
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/nightly-quantum-entanglement-checker

# Build the project
cargo build --release

# Run the tool
cargo run --release -- --help
```

## Usage

### Basic Entanglement Check

```bash
# Generate and verify entangled qubits
cargo run --release -- check --qubits 2 --measurements 1000
```

### Advanced Options

```bash
# Use Hadamard basis and export to JSON
cargo run --release -- check \
  --qubits 2 \
  --measurements 5000 \
  --basis hadamard \
  --output-format json \
  --output-file results.json
```

### Bell Inequality Test

```bash
# Test Bell's inequality violation
cargo run --release -- bell-test \
  --angle-a 0 \
  --angle-b 45 \
  --angle-a-prime 22.5 \
  --angle-b-prime 67.5 \
  --trials 10000
```

## Command Line Options

### `check` Command

- `--qubits <N>`: Number of qubits to simulate (default: 2)
- `--measurements <N>`: Number of measurement trials (default: 1000)
- `--basis <basis>`: Measurement basis - `computational` or `hadamard` (default: computational)
- `--output-format <format>`: Output format - `text`, `json`, or `yaml` (default: text)
- `--output-file <path>`: File to write results to (default: stdout)

### `bell-test` Command

- `--angle-a <deg>`: Measurement angle for Alice (default: 0)
- `--angle-b <deg>`: Measurement angle for Bob (default: 45)
- `--angle-a-prime <deg>`: Alternative measurement angle for Alice (default: 22.5)
- `--angle-b-prime <deg>`: Alternative measurement angle for Bob (default: 67.5)
- `--trials <N>`: Number of Bell test trials (default: 1000)

## Example Output

```
=== Quantum Entanglement Verification Report ===

System Configuration:
  Qubits: 2
  Measurements: 1000
  Basis: Computational
  Timestamp: 2024-01-15T10:30:45Z

Bell State Analysis:
  |Φ⁺⟩ (Phi Plus):  248 measurements (24.8%)
  |Φ⁻⟩ (Phi Minus):  252 measurements (25.2%)
  |Ψ⁺⟩ (Psi Plus):   251 measurements (25.1%)
  |Ψ⁻⟩ (Psi Minus):  249 measurements (24.9%)

Quantum Metrics:
  Fidelity: 0.998
  Concurrence: 0.996
  Entanglement Entropy: 0.999

Bell Inequality Test:
  S-value: 2.828 (Classical limit: 2.0)
  Violation: 41.4% above classical limit
  Result: ✅ QUANTUM ENTANGLEMENT CONFIRMED

Statistical Analysis:
  Chi-square: 0.32
  p-value: 0.956
  Distribution: ✅ CONSISTENT WITH QUANTUM THEORY
```

## Technical Details

### Bell States

The tool simulates the four canonical Bell states:

- **|Φ⁺⟩ = (|00⟩ + |11⟩)/√2** - Both qubits correlated in same state
- **|Φ⁻⟩ = (|00⟩ - |11⟩)/√2** - Both qubits anti-correlated in same state
- **|Ψ⁺⟩ = (|01⟩ + |10⟩)/√2** - Qubits correlated in opposite states
- **|Ψ⁻⟩ = (|01⟩ - |10⟩)/√2** - Qubits anti-correlated in opposite states

### Measurement Bases

- **Computational basis**: Measures in |0⟩/|1⟩ states
- **Hadamard basis**: Measures in |+⟩/|-⟩ states where |+⟩ = (|0⟩ + |1⟩)/√2

### Bell's Inequality

The tool implements the CHSH inequality test with the formula:

```
S = |E(a,b) - E(a,b') + E(a',b) + E(a',b')| ≤ 2
```

Where E represents correlation measurements at different angles.

## Use Cases

1. **Educational**: Learn quantum computing concepts through simulation
2. **Testing**: Verify distributed system behavior under quantum-like constraints
3. **Research**: Prototype quantum algorithm components
4. **Fun**: Generate quantum-themed reports for team meetings

## Dependencies

- Rust 1.70+
- `rand` crate for random number generation
- `serde` and `serde_json` for JSON serialization
- `serde_yaml` for YAML output
- `clap` for command-line argument parsing

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Disclaimer

This tool simulates quantum phenomena for educational and testing purposes. It does not perform actual quantum computations or create real entangled particles. Results are generated using classical random number generation and mathematical models.
