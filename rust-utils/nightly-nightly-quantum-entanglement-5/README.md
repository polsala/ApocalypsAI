# Nightly Quantum Entanglement Checker

Ever wondered if your code files are quantum-entangled across the multiverse? This whimsical-yet-useful utility checks if two files share the same quantum state (hash) with a probabilistic twist!

## Features

- 🌀 **Quantum State Analysis**: Compares file hashes with quantum uncertainty
- 🎲 **Probabilistic Verification**: Adds quantum randomness to the comparison
- 📊 **Entanglement Metrics**: Provides quantum coherence scores
- 🚀 **Blazing Fast**: Written in Rust for maximum performance
- 🧪 **Fully Tested**: Includes comprehensive test suite

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd <repo-url>/rust-utils/nightly-quantum-entanglement-checker

# Build the project
cargo build --release

# Run the binary
cargo run --release -- <file1> <file2>
```

## Usage

```bash
# Check if two files are quantum-entangled
cargo run --release -- file1.txt file2.txt

# With verbose output
cargo run --release -- --verbose file1.txt file2.txt

# Check multiple file pairs
cargo run --release -- --batch file_pairs.txt
```

## Output

The checker will report:

- **Quantum State Match**: Whether the files have identical hashes
- **Entanglement Probability**: Quantum uncertainty percentage
- **Coherence Score**: How well the files maintain quantum coherence
- **Superposition Status**: Whether files exist in superposition

## Examples

```bash
# Check if your config files are entangled
cargo run --release -- config1.json config2.json

# Verify backup integrity
cargo run --release -- original.txt backup.txt

# Batch check multiple files
echo "file1.txt file2.txt" > pairs.txt
echo "backup1.zip backup2.zip" >> pairs.txt
cargo run --release -- --batch pairs.txt
```

## Quantum Theory (Simplified)

In quantum mechanics, entangled particles share states regardless of distance. This tool whimsically applies that concept to file comparison, adding quantum uncertainty to make the process more... interesting.

## License

MIT License - feel free to use this for your quantum computing needs!
