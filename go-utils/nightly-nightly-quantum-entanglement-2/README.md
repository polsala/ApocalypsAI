# Nightly Quantum Entanglement Checker

A whimsical utility that checks if two code files are 'quantum entangled' by comparing their hashes in a fun way. Perfect for verifying file integrity with a touch of quantum physics humor!

## Features

- 🚀 Fast Go-based implementation
- 🔗 Compares file hashes to detect 'quantum entanglement'
- 🎭 Whimsical quantum physics-themed output
- 📊 Displays hash values and comparison results
- 🧪 Includes comprehensive tests

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd <repo-url>/go-utils/nightly-quantum-entanglement-checker

# Build the utility
go build -o qec ./src

# Run the tests
go test ./tests
```

## Usage

```bash
# Check if two files are quantum entangled
./qec file1.txt file2.txt

# Example output:
# 📄 File 1: file1.txt
# Hash: a1b2c3d4e5f6...
# 
# 📄 File 2: file2.txt
# Hash: a1b2c3d4e5f6...
# 
# ✨ Quantum Analysis Complete!
# 🎯 Result: These files are QUANTUM ENTANGLED! 🪐
# 💫 They share the same cosmic signature.
```

## Examples

```bash
# Check identical files
./qec README.md README.md

# Check different files
./qec src/main.go tests/main_test.go

# Check non-existent files (error handling)
./qec nonexistent.txt missing.txt
```

## License

MIT License - feel free to use in your quantum experiments!
