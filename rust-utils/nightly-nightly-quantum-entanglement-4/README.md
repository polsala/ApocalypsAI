# Nightly Quantum Entanglement Checker

Ever wondered if your codebase is quantum-entangled with another repository? This whimsical-yet-useful tool checks for quantum entanglement between two codebases using advanced string similarity algorithms implemented in blazing-fast Rust!

## Features

- 🚀 **Lightning fast** - Rust implementation for maximum performance
- 🌀 **Quantum metaphors** - Entanglement detection with scientific flair
- 📊 **Detailed reports** - Comprehensive similarity analysis
- 🎭 **Whimsical output** - Fun quantum-themed messages
- 📁 **Flexible input** - Compare directories or specific file patterns

## Installation

### Prerequisites
- Rust 1.70+ (install from [rustup.rs](https://rustup.rs/))

### Build from source

```bash
# Clone or download this utility
git clone <repository-url>
cd nightly-quantum-entanglement-checker

# Build in release mode
cargo build --release

# Run the binary
./target/release/quantum-entanglement-checker --help
```

## Usage

### Basic comparison

```bash
# Compare two directories
./target/release/quantum-entanglement-checker --dir1 /path/to/codebase1 --dir2 /path/to/codebase2

# Compare with custom file patterns
./target/release/quantum-entanglement-checker --dir1 /path/to/codebase1 --dir2 /path/to/codebase2 --pattern "*.rs"

# Set minimum entanglement threshold (0.0 to 1.0)
./target/release/quantum-entanglement-checker --dir1 /path/to/codebase1 --dir2 /path/to/codebase2 --threshold 0.8
```

### Example output

```
🔬 Quantum Entanglement Detector v1.0
========================================

📡 Scanning directories for quantum signatures...

📁 Analyzing 153 files in codebase1...
📁 Analyzing 147 files in codebase2...

⚛️  Computing quantum wave functions...

Results:
--------

✅ Quantum Entanglement Detected!

Entanglement Coefficient: 0.87 (STRONG)

Most entangled files:
- src/lib.rs ↔ src/library.rs (92%)
- src/utils.rs ↔ src/helpers.rs (88%)
- tests/integration.rs ↔ tests/e2e.rs (85%)

⚠️  Warning: High probability of code duplication detected!
💡 Recommendation: Consider refactoring shared logic into a common module.

✨ Quantum analysis complete!
```

## Advanced Options

| Option | Description | Default |
|--------|-------------|---------|
| `--dir1` | First directory to compare | - |
| `--dir2` | Second directory to compare | - |
| `--pattern` | File pattern to match (e.g., "*.rs") | "*" |
| `--threshold` | Minimum entanglement threshold (0.0-1.0) | 0.5 |
| `--max-depth` | Maximum directory depth to scan | 10 |
| `--output` | Output format (text/json) | text |
| `--verbose` | Enable verbose logging | false |

## Quantum Theory (The Whimsical Version)

According to our quantum model:

1. **Entanglement Coefficient** measures how "spookily" similar two codebases are
2. **Quantum Superposition** occurs when the same logic exists in multiple places
3. **Wave Function Collapse** happens when we detect identical code patterns

The higher the coefficient, the more likely the codebases share a quantum-entangled past!

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details.

## Disclaimers

⚠️ **Quantum Mechanics Disclaimer**: This tool is for entertainment and code analysis purposes only. It does not actually use quantum computing or detect real quantum entanglement. Any similarities to actual quantum physics are purely coincidental and whimsical.

## Changelog

### v1.0.0
- Initial release
- Basic directory comparison
- Quantum-themed output
- Comprehensive test suite

## Support

If you encounter issues or have suggestions:
- 🐛 [Report bugs](https://github.com/your-repo/issues)
- 💡 [Request features](https://github.com/your-repo/issues)
- 📚 [Ask questions](https://github.com/your-repo/discussions)

May your code be entangled only with good practices! 🚀✨
