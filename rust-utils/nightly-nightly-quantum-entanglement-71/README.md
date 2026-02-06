# Nightly Quantum Entanglement Checker

A whimsical-yet-useful Rust CLI tool that simulates quantum entanglement verification for distributed systems using Bell state measurements. Perfect for testing distributed consensus algorithms and demonstrating quantum computing concepts.

## Features

- Simulates Bell state measurements for entangled qubit pairs
- Generates quantum circuit visualizations
- Provides statistical analysis of measurement outcomes
- Supports both local simulation and networked entanglement scenarios
- Includes educational mode with quantum mechanics explanations

## Installation

### From Crates.io
```bash
cargo install nightly-quantum-entanglement-checker
```

### From Source
```bash
git clone https://github.com/polsala/ApocalypsAI
cd utils/nightly-quantum-entanglement-checker
cargo build --release
```

## Usage

### Basic Entanglement Verification
```bash
# Verify entanglement between two simulated qubits
nightly-quantum-entanglement-checker verify --qubits 2 --measurements 1000

# Output:
# Bell State: |Φ+⟩ = (|00⟩ + |11⟩)/√2
# Measurements: 1000
# Correlation: 0.998 (entangled!)
# CHSH Violation: 2.82 (quantum!)
```

### Networked Entanglement Simulation
```bash
# Simulate entanglement across network nodes
nightly-quantum-entanglement-checker network --nodes 4 --distance 1000

# Output:
# Network Entanglement Status: ✓ Verified
# Decoherence Rate: 0.02%
# Fidelity: 99.8%
```

### Educational Mode
```bash
# Learn about quantum entanglement
nightly-quantum-entanglement-checker learn --concept bell-inequality

# Output:
# Bell's Theorem: Local hidden variables cannot reproduce all quantum predictions
# CHSH Inequality: |E(a,b) - E(a,b') + E(a',b) + E(a',b')| ≤ 2
# Quantum Mechanics: Can achieve up to 2√2 ≈ 2.828
```

### Circuit Visualization
```bash
# Generate quantum circuit diagram
nightly-quantum-entanglement-checker circuit --bell-state phi-plus --output-format ascii

# Output:
# |0⟩───●───M
#       |
# |0⟩───⊕───M
```

## Command Reference

### verify
Verifies quantum entanglement using Bell state measurements.

**Options:**
- `--qubits <N>`: Number of qubits to simulate (default: 2)
- `--measurements <N>`: Number of measurement trials (default: 1000)
- `--bell-state <STATE>`: Bell state to verify (phi-plus, phi-minus, psi-plus, psi-minus)
- `--precision <DECIMALS>`: Decimal precision for output (default: 3)

### network
Simulates entanglement across a network of quantum nodes.

**Options:**
- `--nodes <N>`: Number of network nodes (default: 2)
- `--distance <KM>`: Distance between nodes in kilometers (default: 100)
- `--decoherence <RATE>`: Decoherence rate per km (default: 0.001)
- `--protocol <PROTOCOL>`: Entanglement protocol (direct, swap, purification)

### learn
Provides educational content about quantum mechanics concepts.

**Options:**
- `--concept <CONCEPT>`: Concept to learn (bell-inequality, superposition, decoherence, teleportation)
- `--interactive`: Enable interactive mode with quizzes

### circuit
Generates quantum circuit diagrams.

**Options:**
- `--bell-state <STATE>`: Bell state to visualize
- `--output-format <FORMAT>`: Output format (ascii, unicode, latex)
- `--save <FILE>`: Save diagram to file

## Examples

### Testing Distributed Consensus
```bash
# Simulate quantum-enhanced consensus
nightly-quantum-entanglement-checker verify --qubits 3 --measurements 5000
```

### Educational Workshop
```bash
# Run interactive quantum mechanics workshop
nightly-quantum-entanglement-checker learn --concept superposition --interactive
```

### Performance Benchmarking
```bash
# Benchmark entanglement verification performance
time nightly-quantum-entanglement-checker verify --qubits 10 --measurements 10000
```

## Technical Details

### Bell State Measurements
The tool implements the CHSH (Clauser-Horne-Shimony-Holt) inequality test:

```
S = |E(a,b) - E(a,b') + E(a',b) + E(a',b')|

Classical limit: S ≤ 2
Quantum limit: S ≤ 2√2 ≈ 2.828
```

### Decoherence Modeling
Network simulations include realistic decoherence effects:

```
Fidelity(t) = e^(-γ * d * t)

Where:
- γ = decoherence rate
- d = distance
- t = time
```

### Quantum State Simulation
Uses efficient matrix representations for:
- |Φ+⟩ = (|00⟩ + |11⟩)/√2
- |Φ-⟩ = (|00⟩ - |11⟩)/√2
- |Ψ+⟩ = (|01⟩ + |10⟩)/√2
- |Ψ-⟩ = (|01⟩ - |10⟩)/√2

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

## License

MIT License - see LICENSE file for details.

## Disclaimer

This tool simulates quantum mechanics concepts for educational and testing purposes. It does not provide actual quantum computing capabilities.

## Dependencies

- `rand`: Random number generation for quantum measurements
- `clap`: Command-line argument parsing
- `serde`: Configuration serialization
- `rayon`: Parallel processing for large simulations

## Performance

- 1000 measurements: ~10ms
- 10000 measurements: ~50ms
- Network simulation: ~100ms per 100km

Optimized for educational use with reasonable performance for demonstration purposes.
