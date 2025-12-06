# Nightly Quantum Quip Generator

A whimsical CLI tool that generates quantum-themed programming jokes with deterministic randomness based on input parameters.

## Features

- Generate quantum-themed programming jokes
- Deterministic randomness based on input parameters
- Configurable joke categories (quantum physics, programming, AI)
- Export jokes to various formats (JSON, plain text)
- Command-line interface with interactive mode

## Installation

```bash
# Clone the repository
git clone <repo-url>

cd rust-utils/nightly-quantum-quip-generator

# Build the project
cargo build --release

# Run the CLI
cargo run --release -- --help
```

## Usage

### Basic Usage

```bash
# Generate a random quantum programming joke
cargo run --release --

# Generate a joke with specific seed
cargo run --release -- --seed 42

# Generate a joke from specific category
cargo run --release -- --category quantum
```

### Advanced Usage

```bash
# Export jokes to JSON file
cargo run --release -- --export json --output jokes.json

# Export jokes to plain text file
cargo run --release -- --export text --output jokes.txt

# Generate multiple jokes
cargo run --release -- --count 5

# Interactive mode
cargo run --release -- --interactive
```

### Command Line Options

- `--seed <number>`: Set a specific seed for deterministic randomness
- `--category <quantum|programming|ai>`: Filter jokes by category
- `--count <number>`: Generate multiple jokes
- `--export <json|text>`: Export format
- `--output <file>`: Output file path
- `--interactive`: Start interactive mode
- `--help`: Show help information

## Examples

```bash
# Generate 3 quantum physics jokes with seed 123
cargo run --release -- --seed 123 --category quantum --count 3

# Export 10 random jokes to JSON
cargo run --release -- --count 10 --export json --output my_jokes.json

# Interactive mode for browsing jokes
cargo run --release -- --interactive
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Joke Categories

- **Quantum Physics**: Jokes about superposition, entanglement, and quantum mechanics
- **Programming**: Jokes about coding, debugging, and software development
- **AI**: Jokes about artificial intelligence, machine learning, and robotics

## Technical Details

The generator uses a deterministic pseudo-random number generator (PCG) seeded with user input to ensure reproducible joke sequences. Jokes are stored as templates with placeholders that are filled in based on the generated random values.

## Dependencies

- `clap`: Command-line argument parsing
- `serde`: Serialization framework
- `serde_json`: JSON serialization
- `pcg_rand`: Pseudo-random number generator
- `colored`: Terminal color output
