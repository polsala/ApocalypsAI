# Nightly Quantum Entanglement Checker

A blazing-fast CLI tool to verify quantum entanglement states with precision and style. Perfect for quantum computing researchers, physicists, and curious minds!

## Features

- **Lightning fast**: Built with Rust for maximum performance
- **Multiple verification methods**: Bell state, CHSH inequality, and entanglement entropy
- **Interactive mode**: Real-time entanglement verification
- **Batch processing**: Process multiple quantum states at once
- **Pretty output**: Colorful terminal output with ASCII art

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

### Basic Verification
```bash
# Check a Bell state
quantum-check --state "00 11" --method bell

# Verify CHSH inequality
quantum-check --chsh 0.85

# Calculate entanglement entropy
quantum-check --entropy "[0.707, 0.707]"
```

### Interactive Mode
```bash
quantum-check --interactive
```

### Batch Processing
```bash
quantum-check --batch states.txt
```

## Examples

```bash
# Verify a maximally entangled Bell state
$ quantum-check --state "00 11" --method bell

🔬 Quantum Entanglement Checker
================================

State: |00⟩ + |11⟩
Method: Bell State Verification
Result: ✅ ENTANGLED
Confidence: 100.00%

# Check CHSH inequality violation
$ quantum-check --chsh 0.85

🔬 CHSH Inequality Test
======================

Measured Value: 0.85
Classical Bound: 0.75
Quantum Bound: 0.85355
Result: ✅ VIOLATION DETECTED

# Calculate entanglement entropy
$ quantum-check --entropy "[0.707, 0.707]"

🔬 Entanglement Entropy
=======================

Coefficients: [0.707, 0.707]
Entropy: 1.000 bits
Result: ✅ MAXIMALLY ENTANGLED
```

## License

MIT License - Do whatever you want with it, just don't break spacetime!
