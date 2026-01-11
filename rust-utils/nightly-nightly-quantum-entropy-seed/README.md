# Nightly Quantum Entropy Seeder

A whimsical-yet-useful CLI tool that generates cryptographically strong random seeds using quantum noise from public APIs.

## Features

- Fetches quantum random numbers from ANU's Quantum Random Number Generator API
- Falls back to atmospheric noise from RANDOM.ORG
- Generates seeds in multiple formats (hex, base64, decimal)
- Configurable entropy pool size
- Deterministic seed generation for reproducible results

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd utils/nightly-quantum-entropy-seeder

# Build the tool
cargo build --release

# Run the binary
cargo run --release -- --help
```

## Usage

```bash
# Generate a 256-bit hex seed
./target/release/nightly-quantum-entropy-seeder --format hex --bits 256

# Generate a base64 seed with custom pool size
./target/release/nightly-quantum-entropy-seeder --format base64 --pool-size 100

# Generate a decimal seed with fallback to atmospheric noise
./target/release/nightly-quantum-entropy-seeder --format decimal --fallback atmospheric

# Generate a deterministic seed (useful for testing)
./target/release/nightly-quantum-entropy-seeder --deterministic
```

## Options

- `--format`: Output format (hex, base64, decimal). Default: hex
- `--bits`: Number of bits for the seed. Default: 256
- `--pool-size`: Number of quantum random numbers to fetch. Default: 50
- `--fallback`: Fallback source (quantum, atmospheric). Default: quantum
- `--deterministic`: Generate a deterministic seed for testing
- `--help`: Show help message

## Examples

```bash
# Generate a hex seed for cryptographic use
nightly-quantum-entropy-seeder --format hex --bits 512

# Generate a base64 seed for API keys
nightly-quantum-entropy-seeder --format base64 --bits 128

# Generate a decimal seed for lottery numbers
nightly-quantum-entropy-seeder --format decimal --bits 32
```

## Security Notes

- This tool is for educational and entertainment purposes
- While it uses quantum and atmospheric noise, always verify the entropy quality for cryptographic applications
- The deterministic mode is not suitable for security-critical applications

## Dependencies

- `reqwest`: HTTP client for API requests
- `serde`: Serialization framework
- `serde_json`: JSON serialization
- `base64`: Base64 encoding
- `rand`: Random number generation for fallback
- `anyhow`: Error handling
- `clap`: Command-line argument parsing

## License

MIT License
