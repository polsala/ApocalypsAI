# Nightly Quantum Entanglement Checker

Ever wondered if your code files are quantum-entangled across the multiverse? This whimsical-yet-useful utility checks if two files share the same quantum state (hash) with a probabilistic twist!

## Features

- **Quantum State Verification**: Compares file hashes with a 99.9% confidence level
- **Entanglement Probability**: Shows the likelihood of quantum entanglement
- **Multiverse Detection**: Detects if files exist in parallel universes (different paths)
- **Whimsical Output**: Fun quantum physics-themed messages

## Installation

```bash
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/go-utils/nightly-quantum-entanglement-checker

# Build the binary
go build -o qec ./src

# Run the checker
./qec file1.go file2.go
```

## Usage

```bash
# Check if two files are quantum-entangled
./qec src/main.go src/backup.go

# Output:
# 🌌 Quantum Entanglement Checker 🌌
# File 1: src/main.go
# File 2: src/backup.go
# 
# Quantum State Analysis:
# Hash 1: a1b2c3d4e5f6...
# Hash 2: a1b2c3d4e5f6...
# 
# 🎯 Entanglement Probability: 99.9%
# ✨ These files are quantum-entangled!
# 
# "Spooky action at a distance confirmed." - Einstein

# Check files in parallel universes
./qec /path/to/file.go /different/path/file.go

# Output:
# 🌌 Quantum Entanglement Checker 🌌
# File 1: /path/to/file.go
# File 2: /different/path/file.go
# 
# Quantum State Analysis:
# Hash 1: a1b2c3d4e5f6...
# Hash 2: a1b2c3d4e5f6...
# 
# 🎯 Entanglement Probability: 99.9%
# ✨ These files are quantum-entangled across parallel universes!
# 
# "The universe is not only stranger than we imagine, it is stranger than we can imagine." - Haldane
```

## Why Use This?

- **Fun**: Add some quantum physics humor to your development workflow
- **Verification**: Ensure your backup files or copies are truly identical
- **Education**: Learn about hash functions and quantum entanglement concepts
- **Debugging**: Quickly verify file integrity across different locations

## Technical Details

- Uses SHA-256 hashing for quantum state verification
- Implements probabilistic entanglement detection
- Handles file paths as quantum coordinates in the multiverse
- Provides whimsical quantum physics quotes for each result

## License

MIT - For the quantum community
