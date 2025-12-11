# Nightly Quantum Cache Warmer

A high-performance CLI tool that preloads frequently accessed data into memory using quantum-inspired probabilistic caching algorithms. Perfect for warming up caches before peak traffic or preparing systems for intensive workloads.

## Features

- **Quantum-inspired caching**: Uses probabilistic algorithms inspired by quantum superposition
- **Multi-threaded warming**: Leverages Rust's async capabilities for maximum throughput
- **Configurable strategies**: Choose from multiple warming strategies
- **Real-time metrics**: Monitor cache hit rates and warming performance
- **Zero-config defaults**: Works out of the box with sensible defaults

## Installation

### From Crates.io
```bash
cargo install nightly-quantum-cache-warmer
```

### From Source
```bash
git clone <repo-url>
cd nightly-quantum-cache-warmer
cargo build --release
```

## Usage

### Basic Warming
```bash
# Warm cache with default settings
nightly-quantum-cache-warmer --config config.toml
```

### Advanced Options
```bash
# Custom warming strategy with verbose output
nightly-quantum-cache-warmer \
  --strategy probabilistic \
  --threads 8 \
  --duration 300 \
  --verbose
```

### Configuration File (config.toml)
```toml
[cache]
strategy = "quantum_superposition"
threads = 4
duration = 60

[metrics]
interval = 10
output_format = "json"

[targets]
urls = [
  "https://api.example.com/data",
  "https://api.example.com/users",
  "https://api.example.com/products"
]
```

## Strategies

- **probabilistic**: Uses probability distributions to determine warming patterns
- **sequential**: Linear traversal of cache entries
- **random_walk**: Random access pattern for cache warming
- **quantum_superposition**: Advanced algorithm simulating quantum states

## Output Formats

- **text**: Human-readable console output
- **json**: Machine-readable JSON format
- **csv**: Comma-separated values for analysis

## License

MIT License - see LICENSE file for details.
