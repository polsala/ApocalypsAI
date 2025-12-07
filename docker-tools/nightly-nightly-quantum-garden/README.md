# Nightly Quantum Garden

A whimsical containerized tool that simulates quantum garden growth patterns for stress relief and creative inspiration.

## What is it?

The Nightly Quantum Garden is a Docker-based utility that generates beautiful, procedurally-created quantum garden visualizations. Each run creates a unique garden with:
- Quantum superposition flowers that exist in multiple states
- Entangled butterflies that mirror each other's movements
- Probabilistic growth patterns based on quantum mechanics principles
- Soothing ASCII art visualizations

## Features

- **Containerized**: Run anywhere Docker is supported
- **Deterministic**: Same seed produces same garden (great for reproducibility)
- **Educational**: Includes quantum mechanics concepts explained in simple terms
- **Customizable**: Adjust garden size, growth speed, and quantum effects
- **Offline**: No external dependencies or network calls

## Installation

### Prerequisites

- Docker installed on your system

### Quick Start

```bash
# Build the container
docker build -t nightly-quantum-garden .

# Run with default settings
docker run --rm nightly-quantum-garden

# Run with custom settings
docker run --rm nightly-quantum-garden --size 20 --seed 42 --speed fast
```

## Usage

### Command Line Options

- `--size N`: Garden size (5-50, default: 15)
- `--seed N`: Random seed for reproducible gardens (default: current timestamp)
- `--speed [slow|medium|fast]`: Animation speed (default: medium)
- `--duration N`: Number of growth cycles (default: 10)
- `--help`: Show help message

### Examples

```bash
# Create a small, fast garden with a specific seed
docker run --rm nightly-quantum-garden --size 10 --seed 1337 --speed fast

# Create a large, slow garden for meditation
docker run --rm nightly-quantum-garden --size 30 --speed slow --duration 20

# Save your favorite garden configuration
docker run --rm nightly-quantum-garden --size 18 --seed 9999 > my_favorite_garden.txt
```

## Quantum Concepts Explained

The garden demonstrates these quantum principles in a fun way:

1. **Superposition**: Flowers exist in multiple states until observed
2. **Entanglement**: Butterflies move in mirrored patterns
3. **Quantum Tunneling**: Plants can "tunnel" through barriers
4. **Wave Function Collapse**: Observation affects the garden's state

## Development

### Building Locally

```bash
# Clone or navigate to the utility directory
cd docker-tools/nightly-quantum-garden

# Build the Docker image
docker build -t nightly-quantum-garden .

# Run tests
docker run --rm nightly-quantum-garden python3 /tests/test_garden.py
```

### Testing

The utility includes comprehensive tests that verify:
- Deterministic behavior with seeds
- Garden generation logic
- Quantum effect calculations
- Edge cases and error handling

Run tests with:
```bash
docker run --rm nightly-quantum-garden python3 /tests/test_garden.py
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - see LICENSE file for details

## Acknowledgments

Inspired by quantum mechanics, generative art, and the beauty of nature's complexity.
