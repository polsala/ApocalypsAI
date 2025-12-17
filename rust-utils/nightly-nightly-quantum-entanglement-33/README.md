# Nightly Quantum Entanglement Checker

A whimsical-yet-useful utility that checks if two code snippets are 'quantum entangled' by comparing their hash signatures with a probabilistic twist. Perfect for detecting spooky action at a distance in your codebase!

## Features

- 🚀 Fast Rust implementation with SHA-256 hashing
- 🎲 Probabilistic entanglement detection with configurable uncertainty
- 📊 Detailed similarity reports with quantum metaphors
- 🧪 Comprehensive test suite with mock scenarios
- 🌈 Colorful CLI output with ASCII art

## Installation

```bash
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI

# Build the quantum entanglement checker
cargo build --release --bin nightly-quantum-entanglement-checker

# Run it!
cargo run --release --bin nightly-quantum-entanglement-checker -- --help
```

## Usage

### Basic Entanglement Check

```bash
# Check if two files are quantum entangled
./target/release/nightly-quantum-entanglement-checker \
  --file1 path/to/file1.rs \
  --file2 path/to/file2.rs

# Or pipe content directly
echo "fn hello() { println!(\"world\"); }" | \
./target/release/nightly-quantum-entanglement-checker \
  --stdin --file2 path/to/other.rs
```

### Advanced Options

```bash
# Adjust the quantum uncertainty threshold (0.0 to 1.0)
./target/release/nightly-quantum-entanglement-checker \
  --file1 a.rs --file2 b.rs \
  --uncertainty 0.1

# Enable verbose quantum state reporting
./target/release/nightly-quantum-entanglement-checker \
  --file1 a.rs --file2 b.rs \
  --verbose

# Output in JSON format for machine processing
./target/release/nightly-quantum-entanglement-checker \
  --file1 a.rs --file2 b.rs \
  --format json
```

## Quantum Theory (Simplified)

This utility uses quantum-inspired algorithms to determine if two code snippets share the same quantum state:

1. **Hash Function**: Uses SHA-256 to create a unique quantum signature
2. **Uncertainty Principle**: Introduces probabilistic elements to account for Heisenberg compensation
3. **Entanglement Detection**: Compares quantum states with configurable tolerance
4. **Collapse Simulation**: Simulates wave function collapse for definitive results

## Examples

### Example 1: Identical Code

```bash
# Create two identical files
echo "fn add(a: i32, b: i32) -> i32 { a + b }" > file1.rs
echo "fn add(a: i32, b: i32) -> i32 { a + b }" > file2.rs

# Check entanglement
./target/release/nightly-quantum-entanglement-checker --file1 file1.rs --file2 file2.rs
```

**Output:**
```
🌌 Quantum Entanglement Analysis 🌌

File 1: file1.rs
File 2: file2.rs

🔮 Quantum State Analysis:
- Hash similarity: 100.00%
- Entanglement probability: 100.00%
- Uncertainty threshold: 0.05

✅ CONCLUSION: These files are QUANTUM ENTANGLED!
   Spooky action detected at a distance.
   Wave function collapse: DETERMINISTIC
```

### Example 2: Similar Code

```bash
# Create similar but different files
echo "fn add(a: i32, b: i32) -> i32 { a + b }" > file1.rs
echo "fn add_numbers(x: i32, y: i32) -> i32 { x + y }" > file2.rs

# Check entanglement
./target/release/nightly-quantum-entanglement-checker --file1 file1.rs --file2 file2.rs
```

**Output:**
```
🌌 Quantum Entanglement Analysis 🌌

File 1: file1.rs
File 2: file2.rs

🔮 Quantum State Analysis:
- Hash similarity: 87.50%
- Entanglement probability: 82.50%
- Uncertainty threshold: 0.05

⚠️  CONCLUSION: These files show QUANTUM CORRELATION!
   Similar wave functions detected.
   Further observation recommended.
```

### Example 3: Different Code

```bash
# Create completely different files
echo "fn add(a: i32, b: i32) -> i32 { a + b }" > file1.rs
echo "struct Point { x: f64, y: f64 }" > file2.rs

# Check entanglement
./target/release/nightly-quantum-entanglement-checker --file1 file1.rs --file2 file2.rs
```

**Output:**
```
🌌 Quantum Entanglement Analysis 🌌

File 1: file1.rs
File 2: file2.rs

🔮 Quantum State Analysis:
- Hash similarity: 12.50%
- Entanglement probability: 7.50%
- Uncertainty threshold: 0.05

❌ CONCLUSION: These files are QUANTUM INDEPENDENT!
   No spooky action detected.
   Wave functions remain separate.
```

## Configuration

Create a `quantum.toml` configuration file in your project root:

```toml
[quantum]
# Default uncertainty threshold (0.0 to 1.0)
uncertainty_threshold = 0.05

# Enable verbose quantum state reporting
verbose = false

# Default output format (text, json)
output_format = "text"

# Enable ASCII art in output
ascii_art = true
```

## API Reference

### Command Line Interface

```
USAGE:
    nightly-quantum-entanglement-checker [OPTIONS] --file1 <FILE1> --file2 <FILE2>

FLAGS:
    -h, --help       Print help information
    -V, --version    Print version information

OPTIONS:
    -1, --file1 <FILE1>              First file to compare
    -2, --file2 <FILE2>              Second file to compare
    -f, --format <FORMAT>            Output format [possible values: text, json]
    -s, --stdin                      Read first file from stdin
    -u, --uncertainty <UNCERTAINTY>  Quantum uncertainty threshold [default: 0.05]
    -v, --verbose                    Enable verbose quantum state reporting
```

### Programmatic Usage

```rust
use nightly_quantum_entanglement_checker::{QuantumAnalyzer, EntanglementResult};

let analyzer = QuantumAnalyzer::new();

let result = analyzer.analyze_files(
    "path/to/file1.rs",
    "path/to/file2.rs",
    0.05 // uncertainty threshold
).await?;

match result.entanglement_state {
    EntanglementState::Entangled => println!("Quantum entanglement detected!"),
    EntanglementState::Correlated => println!("Quantum correlation detected!"),
    EntanglementState::Independent => println!("No quantum relationship detected."),
}
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
cargo test

# Run specific test categories
cargo test quantum_physics
cargo test file_handling
cargo test cli_interface

# Run with coverage (if available)
cargo tarpaulin --out Html
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/quantum-improvements`)
3. Commit your changes (`git commit -m 'Add quantum improvements'`)
4. Push to the branch (`git push origin feature/quantum-improvements`)
5. Create a Pull Request

### Quantum Development Guidelines

- All new features must include quantum-themed documentation
- Tests must cover edge cases with appropriate uncertainty
- Code must pass quantum linting standards
- Maintain backward compatibility for existing quantum states

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.

## Quantum Disclaimers

⚠️ **Important**: This utility is for entertainment and educational purposes only. It does not actually perform quantum computing or detect real quantum entanglement. Any spooky action at a distance is purely metaphorical.

🔮 **Quantum Guarantee**: We do not guarantee the accuracy of quantum state predictions. Results may be subject to the uncertainty principle.

🌌 **Cosmic Responsibility**: Use this tool wisely. With great quantum power comes great quantum responsibility.

## Acknowledgments

- Thanks to Schrödinger for the cat metaphor
- Thanks to Heisenberg for the uncertainty principle
- Thanks to Einstein for the "spooky action at a distance" quote
- Thanks to all the quantum physicists who made this whimsical tool possible

## Changelog

### v1.0.0 (2024-01-01)

- Initial release of the Quantum Entanglement Checker
- Implemented SHA-256 hashing for quantum signatures
- Added probabilistic entanglement detection
- Included comprehensive test suite
- Added support for multiple output formats

## Support

If you encounter quantum anomalies or have questions:

1. Check the [Issues](https://github.com/polsala/ApocalypsAI/issues) page
2. Create a new issue with detailed quantum state information
3. Include your wave function collapse logs
4. Tag with `quantum-bug` or `quantum-feature`

**Remember**: In the quantum world of software, observation affects the observed. Please provide detailed reproduction steps!
