# Nightly Quantum Entanglement Checker

![Quantum](https://img.shields.io/badge/Quantum-Spooky%20Action%20at%20a%20Distance-purple)

Ever wondered if your code files are quantum-entangled? This utility checks if two files are identical and provides a whimsical quantum-themed report!

## Features

- ✨ **Quantum Entanglement Detection**: Checks if two files are identical
- 🎭 **Whimsical Reports**: Spooky quantum-themed output
- 🚀 **Blazing Fast**: Written in Rust for maximum performance
- 🧪 **Well Tested**: Comprehensive test suite included
- 📊 **Detailed Analysis**: Provides file metadata and comparison results

## Installation

### From Source (Rust)

```bash
# Clone or download this utility
# Navigate to the directory
# Build and install
cargo build --release

# Or run directly
cargo run --release -- <file1> <file2>
```

## Usage

### Basic Comparison

```bash
# Compare two files
./target/release/nightly-quantum-entanglement-checker file1.txt file2.txt

# Or using cargo
cargo run --release -- file1.txt file2.txt
```

### Example Output

```
🔬 Quantum Entanglement Checker 🧪

File 1: file1.txt
  📏 Size: 1.2 KB
  🕐 Modified: 2024-01-15 14:30:22 UTC
  🔍 SHA-256: a1b2c3d4e5f6...

File 2: file2.txt
  📏 Size: 1.2 KB
  🕐 Modified: 2024-01-15 14:30:25 UTC
  🔍 SHA-256: a1b2c3d4e5f6...

🎉 QUANTUM ENTANGLEMENT DETECTED! 🎉

The files are quantum-entangled (identical)!
Spooky action at a distance confirmed. ✨
```

### Non-Entangled Files

```
🔬 Quantum Entanglement Checker 🧪

File 1: file1.txt
  📏 Size: 1.2 KB
  🕐 Modified: 2024-01-15 14:30:22 UTC
  🔍 SHA-256: a1b2c3d4e5f6...

File 2: different.txt
  📏 Size: 1.5 KB
  🕐 Modified: 2024-01-15 14:35:10 UTC
  🔍 SHA-256: f6e5d4c3b2a1...

❌ QUANTUM ENTANGLEMENT NOT FOUND

The files are not quantum-entangled (different).
No spooky action detected today. 👻
```

## Command Line Options

```bash
# Show help
cargo run --release -- --help

# Compare files with verbose output
cargo run --release -- --verbose file1.txt file2.txt
```

## Use Cases

- **Code Synchronization**: Verify files across different systems
- **Backup Verification**: Ensure backup files match originals
- **Deployment Checks**: Confirm deployed files are correct
- **Development Debugging**: Check if files were modified as expected
- **Quantum Computing**: Just for fun! 🎭

## Technical Details

- **Algorithm**: SHA-256 hashing for reliable comparison
- **Performance**: Rust implementation for speed
- **Memory**: Efficient streaming for large files
- **Cross-Platform**: Works on Linux, macOS, and Windows

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/spooky-improvements`
3. Commit your changes: `git commit -m 'Add spooky quantum features'`
4. Push to the branch: `git push origin feature/spooky-improvements`
5. Create a Pull Request

## License

MIT License - see LICENSE file for details.

## Quantum Disclaimer

This utility uses classical computing to check file equality. Real quantum entanglement may require actual quantum computers and is not guaranteed. Spooky action at a distance not included. ✨

## Changelog

### v1.0.0
- Initial release with quantum entanglement detection
- SHA-256 hashing for reliable comparison
- Whimsical quantum-themed output
- Comprehensive test suite

---

**Note**: This utility is part of the ApocalypsAI project - a collection of whimsical-yet-useful tools for the community.
