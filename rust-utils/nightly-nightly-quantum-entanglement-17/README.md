# Nightly Quantum Entanglement Checker

A whimsical CLI tool that checks if two code snippets are 'quantum entangled' by comparing their hash signatures with a playful twist. Perfect for verifying code relationships in a fun way!

## Features

- 🚀 Fast Rust implementation
- 🔗 Compares code snippets using SHA-256 hashes
- 🎭 Whimsical quantum-themed output
- 📊 Shows similarity percentages
- 🧪 Comprehensive test suite

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd nightly-quantum-entanglement-checker

# Build the project
cargo build --release

# Run the tool
cargo run --release --
```

## Usage

```bash
# Check entanglement between two files
cargo run --release -- check file1.rs file2.rs

# Check entanglement with inline code
cargo run --release -- check-inline "fn main() {}" "fn main() { println!(\"hello\"); }"

# Generate quantum report
cargo run --release -- report file1.rs file2.rs
```

## Examples

```bash
# Check if two Rust files are entangled
cargo run --release -- check src/main.rs src/lib.rs

# Compare inline code snippets
cargo run --release -- check-inline "let x = 5;" "let y = 10;"

# Generate a detailed quantum report
cargo run --release -- report src/main.rs src/lib.rs
```

## Output

The tool will display:
- Quantum entanglement status (Entangled/Not Entangled)
- Hash signatures of both code snippets
- Similarity percentage
- Whimsical quantum-themed messages

## License

MIT
