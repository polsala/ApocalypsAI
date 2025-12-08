# Nightly Quantum Entanglement Checker

Ever wondered if two pieces of code are quantum entangled? This whimsical-yet-useful tool checks if two code snippets share the same quantum state by comparing their hash signatures with a probabilistic twist!

## Features

- 🚀 Fast Rust implementation with SHA-256 hashing
- 🌀 Quantum probability simulation (with a 1% chance of false positives)
- 🎭 Whimsical quantum-themed output
- 🧪 Comprehensive test suite with deterministic mocks
- 📦 Zero external dependencies beyond standard library

## Installation

```bash
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-quantum-entanglement-checker

# Build the project
cargo build --release
```

## Usage

```bash
# Check if two files are quantum entangled
cargo run --release -- file1.rs file2.rs

# Check if two strings are quantum entangled
cargo run --release -- --string "Hello World" "Hello World"

# Check with verbose quantum state information
cargo run --release -- --verbose file1.rs file2.rs
```

## Output

The tool will output one of the following quantum states:

- **Quantum Entanglement Confirmed!** 🌀 The code snippets are entangled
- **Quantum Decoherence Detected** ❄️ The code snippets are not entangled
- **Quantum Superposition State** ⚛️ Uncertain due to quantum fluctuations

## Examples

```bash
# Example 1: Identical files
cargo run --release -- src/main.rs src/main.rs
# Output: Quantum Entanglement Confirmed! 🌀

# Example 2: Different files
cargo run --release -- src/main.rs Cargo.toml
# Output: Quantum Decoherence Detected ❄️

# Example 3: String comparison
cargo run --release -- --string "fn main() {}" "fn main() {}"
# Output: Quantum Entanglement Confirmed! 🌀
```

## Quantum Mechanics Disclaimer

This tool is for entertainment purposes only. Real quantum entanglement involves subatomic particles, not code snippets. But wouldn't it be cool if our code could be quantum entangled?

## License

MIT License - see LICENSE file for details.
