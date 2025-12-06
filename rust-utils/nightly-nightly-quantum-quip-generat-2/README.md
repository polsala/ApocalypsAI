# Nightly Quantum Quip Generator

A whimsical CLI tool that generates quantum computing puns and jokes with concurrent processing. Perfect for breaking the ice at tech meetups or debugging sessions!

## Features

- Generates quantum-themed puns and jokes
- Concurrent processing for fast joke delivery
- Configurable output formats (plain text, JSON)
- Interactive mode for continuous joke streaming
- Built with Rust for blazing-fast performance

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd <repo-url>

# Build the project
cargo build --release

# Run the binary
cargo run --release -- --help
```

## Usage

### Basic Usage
```bash
# Generate a single joke
cargo run --release

# Generate multiple jokes
cargo run --release --count 5
```

### Output Formats
```bash
# Plain text output (default)
cargo run --release --format text

# JSON output for programmatic use
cargo run --release --format json
```

### Interactive Mode
```bash
# Stream jokes continuously (press Ctrl+C to stop)
cargo run --release --interactive
```

### Advanced Options
```bash
# Set custom seed for reproducible jokes
cargo run --release --seed 42

# Use multiple threads for joke generation
cargo run --release --threads 4
```

## Examples

```
$ cargo run --release

Quantum Quip: Why don't quantum physicists ever argue? Because they always find themselves in superposition!

$ cargo run --release --format json

{
  "joke": "What do you call a quantum computer that tells jokes? A super-computer!",
  "category": "puns",
  "difficulty": "quantum"
}

$ cargo run --release --interactive

Streaming quantum quips... (Press Ctrl+C to stop)

Quantum Quip: I tried to make a quantum joke, but it collapsed into a pun!
Quantum Quip: Why was Schrödinger's cat such a bad comedian? It couldn't decide if the punchline was funny or not!
Quantum Quip: How many qubits does it take to change a lightbulb? Superpositionally, all of them and none at the same time!
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

Thanks to the quantum computing community for providing endless material for puns and jokes!

---

*This tool is purely for entertainment purposes. No quantum computers were harmed in the making of this utility.*
