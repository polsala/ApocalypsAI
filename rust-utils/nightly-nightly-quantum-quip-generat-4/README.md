# Nightly Quantum Quip Generator

A whimsical CLI tool that generates quantum-themed programming jokes with a configurable probability engine. Perfect for breaking the ice at tech meetups or adding some quantum humor to your daily standups!

## Features

- Generates quantum-themed programming jokes
- Configurable probability engine for joke selection
- Command-line interface with optional custom seed
- Unit tests with deterministic mocking

## Installation

Requires Rust 1.70+ and Cargo.

```bash
# Clone or copy the source files
# Build the project
cargo build --release

# Run the generator
cargo run --release

# Or with a custom seed
cargo run --release -- --seed 42
```

## Usage

```bash
# Generate a random quantum quip
cargo run --release

# Generate with a specific seed for reproducible output
cargo run --release -- --seed 12345

# Get help
cargo run --release -- --help
```

## Example Output

```
Why do quantum programmers never make decisions?
Because they exist in a superposition of both committing and not committing until observed!
```

## License

MIT
