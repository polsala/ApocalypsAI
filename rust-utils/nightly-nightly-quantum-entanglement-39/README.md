# Nightly Quantum Entanglement Checker

A whimsical-yet-useful Rust CLI tool that simulates quantum entanglement verification for distributed systems using Bell's inequality tests. Perfect for testing distributed system reliability and adding some quantum flair to your workflow!

## Features

- Simulates quantum entanglement verification using Bell's inequality
- Generates entanglement reports with statistical analysis
- Supports both local and distributed entanglement scenarios
- Whimsical quantum-themed output with ASCII art
- Fast, single-binary Rust implementation

## Installation

### From Source

```bash
# Clone the repository
git clone <repository-url>
cd utils/nightly-quantum-entanglement-checker

# Build the project
cargo build --release

# Run the tool
cargo run --release -- --help
```

### Binary Distribution

Download the pre-built binary from the releases page and add it to your PATH.

## Usage

```bash
# Basic entanglement check
nightly-quantum-entanglement-checker --particles 1000 --trials 100

# Distributed entanglement scenario
nightly-quantum-entanglement-checker --distributed --distance 1000 --particles 500

# Custom Bell test parameters
nightly-quantum-entanglement-checker --angle-a 22.5 --angle-b 67.5 --particles 2000

# Generate detailed report
nightly-quantum-entanglement-checker --report --output entanglement_report.txt
```

## Command Line Options

- `--particles N`: Number of simulated particles (default: 1000)
- `--trials N`: Number of measurement trials (default: 100)
- `--angle-a DEG`: Measurement angle for detector A (default: 0.0)
- `--angle-b DEG`: Measurement angle for detector B (default: 45.0)
- `--distributed`: Enable distributed entanglement scenario
- `--distance KM`: Distance between entangled particles in kilometers (default: 100)
- `--report`: Generate detailed entanglement report
- `--output FILE`: Output file for report (default: stdout)
- `--seed N`: Random seed for reproducible results
- `--help, -h`: Show help message

## Examples

### Basic Usage

```bash
# Run a basic entanglement verification
nightly-quantum-entanglement-checker --particles 10000 --trials 50
```

### Distributed System Testing

```bash
# Simulate entanglement across a distributed system
nightly-quantum-entanglement-checker --distributed --distance 5000 --particles 5000
```

### Scientific Analysis

```bash
# Generate a detailed report for scientific analysis
nightly-quantum-entanglement-checker --report --output quantum_analysis.txt --particles 50000
```

## Output Format

The tool outputs a quantum-themed report including:

- Bell inequality violation statistics
- Entanglement correlation coefficients
- Measurement outcome distributions
- Quantum state fidelity analysis
- ASCII art representations of quantum states

## Performance

- **Speed**: Rust implementation processes millions of particles efficiently
- **Memory**: Minimal memory footprint with streaming calculations
- **Accuracy**: High-precision floating-point calculations for scientific accuracy

## Use Cases

- **Educational**: Demonstrate quantum mechanics concepts
- **Testing**: Verify distributed system reliability
- **Scientific**: Simulate quantum experiments
- **Fun**: Add quantum flair to your development workflow

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please follow standard Rust conventions and include tests for new features.

## Disclaimer

This tool simulates quantum entanglement for educational and testing purposes. It does not create actual quantum states or violate any physical laws. Use responsibly and enjoy the quantum journey!
