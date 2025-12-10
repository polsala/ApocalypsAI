# Nightly Quantum Entanglement Checker

A whimsical utility that checks if two code snippets are 'quantum entangled' by comparing their hashes and generating a fun entanglement report.

## Features

- **Quantum Entanglement Detection**: Compares code snippets using SHA-256 hashes
- **Whimsical Reports**: Generates fun entanglement reports with quantum-themed messages
- **CLI Interface**: Easy-to-use command-line tool
- **Deterministic Testing**: Includes comprehensive unit tests with mocks

## Installation

```bash
# Clone the repository
git clone <repo-url>

cd nightly-quantum-entanglement-checker

# Build the project
cargo build --release

# Run the utility
./target/release/quantum-entanglement-checker --help
```

## Usage

```bash
# Check if two files are entangled
./target/release/quantum-entanglement-checker file1.rs file2.rs

# Check if two strings are entangled
./target/release/quantum-entanglement-checker --string "Hello World" --string "Hello World"

# Generate a quantum report
./target/release/quantum-entanglement-checker --report file1.rs file2.rs
```

## Examples

```bash
# Example 1: Check identical files
./target/release/quantum-entanglement-checker src/main.rs src/main.rs

# Example 2: Check different files
./target/release/quantum-entanglement-checker src/main.rs src/lib.rs

# Example 3: Check strings
./target/release/quantum-entanglement-checker --string "quantum" --string "quantum"
```

## Quantum Entanglement Report

When using the `--report` flag, the utility generates a whimsical quantum entanglement report:

```
🔬 Quantum Entanglement Analysis Report 🔬
==========================================

File A: src/main.rs
File B: src/main.rs

✅ ENTANGLEMENT CONFIRMED!

Both particles (files) share identical quantum states.
The universe has spoken: these code snippets are entangled.

Quantum Coherence Level: MAXIMUM
Spooky Action at Distance: DETECTED

Recommendation: Keep these particles together for optimal quantum computing performance.
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This utility is for entertainment purposes only. It does not actually perform quantum entanglement detection. Any resemblance to real quantum physics is purely coincidental.
