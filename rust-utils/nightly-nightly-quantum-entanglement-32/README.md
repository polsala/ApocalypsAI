# Nightly Quantum Entanglement Checker

A whimsical-yet-useful Rust utility that checks if two code snippets are 'quantum entangled' by comparing their hash signatures with a probabilistic twist.

## Features

- 🚀 Fast Rust implementation with SHA-256 hashing
- 🌀 Quantum-inspired probabilistic comparison
- 🎲 Configurable 'quantum uncertainty' factor
- 📊 Detailed entanglement report with confidence levels
- 🧪 Comprehensive test suite with mock scenarios

## Installation

```bash
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI

# Build the quantum entanglement checker
cargo build --release --bin nightly-quantum-entanglement-checker

# Run the binary
cargo run --release --bin nightly-quantum-entanglement-checker -- --help
```

## Usage

```bash
# Check entanglement between two files
./target/release/nightly-quantum-entanglement-checker \
  --file1 path/to/code1.rs \
  --file2 path/to/code2.rs \
  --uncertainty 0.1

# Check entanglement between two strings
./target/release/nightly-quantum-entanglement-checker \
  --text1 "fn hello() { println!(\"world\"); }" \
  --text2 "fn hello() { println!(\"world\"); }" \
  --uncertainty 0.05

# Generate a detailed quantum report
./target/release/nightly-quantum-entanglement-checker \
  --file1 src/main.rs \
  --file2 src/lib.rs \
  --report output/quantum_report.json
```

## Quantum Uncertainty

The `--uncertainty` parameter (0.0 to 1.0) controls the 'quantum uncertainty' of the comparison:

- **0.0**: Classical deterministic comparison (identical hashes required)
- **0.1**: Slight quantum fuzziness (90% hash similarity required)
- **0.5**: Highly uncertain quantum state (50% hash similarity required)

## Output

The checker provides a detailed quantum report:

```
🔬 Quantum Entanglement Analysis Report
==========================================

Source A: src/main.rs
Source B: src/lib.rs

Hash A: a1b2c3d4e5f6...
Hash B: a1b2c3d4e5f7...

Hamming Distance: 3
Similarity Score: 96.875%
Quantum Threshold: 90.0%

✅ QUANTUM ENTANGLEMENT DETECTED!
Confidence Level: HIGH (96.875%)

Recommendation: These code snippets are quantumly entangled.
```

## Examples

### Example 1: Identical Code

```bash
echo 'fn add(a: i32, b: i32) -> i32 { a + b }' > code1.rs
echo 'fn add(a: i32, b: i32) -> i32 { a + b }' > code2.rs

./target/release/nightly-quantum-entanglement-checker \
  --file1 code1.rs \
  --file2 code2.rs
```

**Result**: Perfect entanglement (100% similarity)

### Example 2: Similar Code with Minor Differences

```bash
echo 'fn add(a: i32, b: i32) -> i32 { a + b }' > code1.rs
echo 'fn add(a: i32, b: i32) -> i32 { b + a }' > code2.rs

./target/release/nightly-quantum-entanglement-checker \
  --file1 code1.rs \
  --file2 code2.rs \
  --uncertainty 0.1
```

**Result**: Quantum entanglement detected (high similarity with quantum uncertainty)

### Example 3: Completely Different Code

```bash
echo 'fn main() { println!("Hello World"); }' > code1.rs
echo 'struct Point { x: f64, y: f64; }' > code2.rs

./target/release/nightly-quantum-entanglement-checker \
  --file1 code1.rs \
  --file2 code2.rs
```

**Result**: No quantum entanglement detected

## Use Cases

- **Code Duplication Detection**: Find similar code patterns across your codebase
- **Plagiarism Detection**: Check if code has been copied with minor modifications
- **Code Evolution Tracking**: Monitor how code changes over time
- **Security Analysis**: Detect similar vulnerable patterns
- **Educational Tool**: Demonstrate hash-based comparison concepts

## Technical Details

### Algorithm

1. **Hash Generation**: SHA-256 hash of each code snippet
2. **Hamming Distance**: Calculate bit-level differences between hashes
3. **Similarity Score**: Convert Hamming distance to percentage similarity
4. **Quantum Threshold**: Apply user-configured uncertainty factor
5. **Entanglement Decision**: Compare similarity against threshold

### Performance

- **Hashing**: SHA-256 provides cryptographic security
- **Comparison**: O(1) hash comparison with O(n) Hamming distance calculation
- **Memory**: Minimal footprint, processes files in chunks

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/quantum-improvements`
3. Commit your changes: `git commit -m 'Add quantum improvements'`
4. Push to the branch: `git push origin feature/quantum-improvements`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

## Quantum Disclaimer

⚠️ **Important**: This tool uses quantum-inspired metaphors for educational and entertainment purposes. It does not actually manipulate quantum states or entangle particles. Any quantum effects are purely computational and metaphorical.

## Support

If you encounter issues or have suggestions:

1. Check the [Issues](https://github.com/polsala/ApocalypsAI/issues) section
2. Create a new issue with:
   - Detailed description of the problem
   - Steps to reproduce
   - Expected vs. actual behavior
   - System information (OS, Rust version)

## Acknowledgments

- Thanks to the Rust community for providing excellent hashing and CLI libraries
- Inspiration from quantum computing research (though we're not actually doing quantum computing here!)
- The concept of quantum entanglement in physics, which inspired this whimsical approach to code comparison
