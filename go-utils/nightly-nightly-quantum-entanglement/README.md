# Nightly Quantum Entanglement Checker

Ever wondered if your code files are quantum-entangled across the multiverse? This whimsical-yet-useful utility checks if two files are identical using Go's concurrency features, complete with quantum-themed output!

## Features

- **Quantum-themed output**: Get results with quantum physics terminology
- **Concurrent processing**: Uses Go's goroutines for efficient file comparison
- **Checksum verification**: Generates SHA-256 hashes for both files
- **Entanglement probability**: Displays a fun "quantum entanglement probability" score
- **Superposition states**: Shows file states in quantum terms

## Installation

### Prerequisites
- Go 1.20 or later

### Build from source

```bash
# Clone or download this utility
# Navigate to the directory
# Build the binary
go build -o quantum-entanglement-checker

# Run the utility
./quantum-entanglement-checker <file1> <file2>
```

## Usage

```bash
# Basic usage
./quantum-entanglement-checker file1.txt file2.txt

# Check if two Go files are entangled
./quantum-entanglement-checker main.go backup.go

# Compare configuration files
./quantum-entanglement-checker config.json config.backup.json
```

## Example Output

```
🔬 Quantum Entanglement Analysis Report 🔬
==========================================

File 1: file1.txt
  📄 Schrödinger State: Collapsed (Classical)
  🔗 Quantum Signature: a1b2c3d4e5f6...
  ⚖️  Wave Function: Stable

File 2: file2.txt
  📄 Schrödinger State: Collapsed (Classical)
  🔗 Quantum Signature: a1b2c3d4e5f6...
  ⚖️  Wave Function: Stable

🔬 Entanglement Analysis:
  🌀 Quantum Correlation: 100.00%
  🌀 Entanglement Status: ✨ QUANTUM ENTANGLEMENT DETECTED ✨
  🌀 Coherence Level: Perfect

💡 Interpretation:
  These files exist in a perfectly entangled quantum state.
  Any measurement on one will instantaneously affect the other!
```

## How It Works

1. **Concurrent Hashing**: Two goroutines hash each file simultaneously
2. **Quantum State Analysis**: Analyzes file properties using quantum metaphors
3. **Entanglement Calculation**: Compares hashes and calculates entanglement probability
4. **Superposition Reporting**: Displays results with quantum physics terminology

## License

MIT License - see LICENSE file for details.

---

*Note: This tool uses actual cryptographic hashing, not actual quantum mechanics.
Any resemblance to real quantum physics is purely for entertainment purposes.*
