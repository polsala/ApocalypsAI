# Nightly Quantum Quip Generator

A whimsical CLI tool that generates quantum-themed programming jokes and puns with configurable randomness and export options.

## Features

- Generate quantum-themed programming jokes and puns
- Configurable randomness for different humor styles
- Export jokes to various formats (JSON, plain text)
- Interactive mode for live joke generation
- Type-safe implementation in Rust

## Installation

```bash
# Clone the repository
git clone <repo-url>

cd utils/nightly-quantum-quip-generator

# Build the project
cargo build --release

# Run the executable
./target/release/nightly-quantum-quip-generator
```

## Usage

### Basic Usage

```bash
# Generate a random quantum quip
./target/release/nightly-quantum-quip-generator

# Generate multiple quips
./target/release/nightly-quantum-quip-generator --count 5

# Export to JSON
./target/release/nightly-quantum-quip-generator --export json --output jokes.json

# Export to plain text
./target/release/nightly-quantum-quip-generator --export text --output jokes.txt
```

### Interactive Mode

```bash
# Start interactive mode
./target/release/nightly-quantum-quip-generator --interactive

# In interactive mode:
# - Press Enter to generate a new joke
# - Type 'exit' to quit
# - Type 'help' for available commands
```

### Configuration

The tool supports different humor styles:

- `quantum` - Classic quantum physics puns
- `programming` - Programming-specific jokes
- `mixed` - A blend of both (default)

```bash
# Generate programming-themed jokes
./target/release/nightly-quantum-quip-generator --style programming

# Generate pure quantum physics jokes
./target/release/nightly-quantum-quip-generator --style quantum
```

## Examples

```
Why don't quantum programmers ever make decisions?
Because they exist in a superposition of states until observed!

What do you call a quantum computer that tells jokes?
A qubit of humor!

Why did Schrödinger's cat start a coding blog?
Because it wanted to share its thoughts on being both alive and dead in the tech world!
```

## License

MIT License

## Contributing

Feel free to submit pull requests with new quantum jokes or improvements!
