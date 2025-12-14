# Nightly Quantum Entanglement Checker

A whimsical utility that checks if two code snippets are 'quantum entangled' by comparing their hash signatures with a playful twist.

## Features

- Generate quantum signatures for code snippets
- Compare signatures to detect entanglement
- Whimsical quantum-themed output messages
- Fast and concurrent processing

## Installation

```bash
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git

cd ApocalypsAI/go-utils/nightly-quantum-entanglement-checker

# Build the binary
go build -o qec ./src

# Run the program
./qec --help
```

## Usage

```bash
# Check entanglement between two files
./qec check file1.go file2.go

# Generate quantum signature for a file
./qec signature file.go

# Compare two signatures
./qec compare sig1.txt sig2.txt
```

## Examples

```bash
# Check if two Go files are quantum entangled
./qec check src/main.go src/utils.go

# Output:
# 🌀 Quantum Analysis Complete!
# File: src/main.go
# Signature: 0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b
# File: src/utils.go
# Signature: 0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b
# 🎉 These files are quantum entangled!
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request
