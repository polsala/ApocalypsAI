# Nightly Quantum Entanglement Checker

Ever wondered if your files are quantumly entangled? This utility simulates quantum entanglement for file pairs, ensuring they remain 'entangled' across operations. Perfect for ensuring your paired files (like config files and their backups) stay in sync!

## Features

- Simulates quantum entanglement for file pairs
- Detects when files have been 'measured' (modified) independently
- Provides whimsical quantum-themed status messages
- Ensures file pairs remain synchronized

## Installation

### Prerequisites
- Rust and Cargo (https://rustup.rs/)

### Build from source
```bash
# Clone or download this utility
# Navigate to the directory
# Build the utility
cargo build --release

# The binary will be at: target/release/nightly-quantum-entanglement-checker
```

## Usage

### Basic Usage
```bash
# Check if two files are entangled
cargo run --release -- --files file1.txt file2.txt

# Check entanglement with custom threshold
cargo run --release -- --files file1.txt file2.txt --threshold 0.8

# Entangle files (create entanglement record)
cargo run --release -- --entangle file1.txt file2.txt

# List all entangled pairs
cargo run --release -- --list

# Clean up entanglement records
cargo run --release -- --clean
```

### Advanced Usage
```bash
# Check multiple file pairs at once
cargo run --release -- --batch pairs.txt

# Output in JSON format for automation
cargo run --release -- --files file1.txt file2.txt --format json

# Set custom entanglement strength
cargo run --release -- --entangle file1.txt file2.txt --strength 0.95
```

### Batch Mode
Create a `pairs.txt` file with one file pair per line:
```
file1.txt file2.txt
config.json config.backup.json
script.sh script.sh.bak
```

Then run:
```bash
cargo run --release -- --batch pairs.txt
```

## Examples

### Example 1: Basic Entanglement Check
```bash
# Create two test files
echo "Hello World" > file1.txt
echo "Hello World" > file2.txt

# Entangle them
cargo run --release -- --entangle file1.txt file2.txt

# Check their entanglement status
cargo run --release -- --files file1.txt file2.txt
```

### Example 2: Detecting Independent Modification
```bash
# Modify one file independently
echo "Modified" >> file1.txt

# Check entanglement - should show decoherence
cargo run --release -- --files file1.txt file2.txt
```

### Example 3: Batch Processing
```bash
# Create multiple file pairs
echo "config.json config.backup.json" > pairs.txt
echo "script.sh script.sh.bak" >> pairs.txt

# Check all pairs at once
cargo run --release -- --batch pairs.txt
```

## Output Formats

### Console Output
```
🔬 Quantum Entanglement Analysis
================================

File Pair: file1.txt ↔ file2.txt
Entanglement Status: ✅ Coherent
Entanglement Strength: 0.95
Quantum Correlation: 0.98
Decoherence Risk: Low

🔮 Quantum State: Superposition maintained
✨ Entanglement verified across all dimensions
```

### JSON Output
```json
{
  "files": ["file1.txt", "file2.txt"],
  "entangled": true,
  "strength": 0.95,
  "correlation": 0.98,
  "decoherence_risk": "low",
  "status": "coherent",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Quantum Concepts (Whimsical Interpretation)

- **Entanglement**: Files are linked and should maintain similar properties
- **Coherence**: Files are in sync and properly entangled
- **Decoherence**: Files have been modified independently, breaking entanglement
- **Quantum Correlation**: How similar the files are (0.0 to 1.0)
- **Measurement**: When a file is modified, it's like measuring a quantum state

## Configuration

### Environment Variables
- `QUANTUM_ENTANGLEMENT_THRESHOLD`: Default threshold for entanglement detection (default: 0.7)
- `QUANTUM_ENTANGLEMENT_DEBUG`: Enable debug output (default: false)

### Configuration File
Create a `.quantum-entanglement.toml` file:
```toml
[entanglement]
threshold = 0.8
strength = 0.95

[output]
format = "json"
verbose = true
```

## Troubleshooting

### Common Issues

1. **Files not found**: Ensure both files exist and paths are correct
2. **Permission denied**: Check file read permissions
3. **Entanglement broken**: Files have been modified independently

### Debug Mode
```bash
# Enable debug output
QUANTUM_ENTANGLEMENT_DEBUG=true cargo run --release -- --files file1.txt file2.txt
```

### Re-entangling Files
```bash
# If files have decohered, re-entangle them
cargo run --release -- --entangle file1.txt file2.txt

# Or copy content to synchronize
cp file1.txt file2.txt
cargo run --release -- --files file1.txt file2.txt
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues, questions, or quantum phenomena, please open an issue on GitHub.

---

**Note**: This utility is for entertainment and educational purposes. It does not actually create quantum entanglement, but provides a fun way to track file synchronization!
