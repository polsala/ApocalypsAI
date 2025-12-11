# Nightly Quantum Entanglement Checker

A whimsical-yet-useful utility that simulates quantum entanglement between files for fun and potentially useful file correlation analysis.

## Features

- Simulates quantum entanglement between files using quantum-inspired algorithms
- Generates entanglement scores between file pairs
- Visualizes entanglement networks
- Cross-platform CLI tool with Rust core and Node.js interface

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd nightly-quantum-entanglement-checker

# Build the Rust core
cargo build --release

# Install Node.js CLI
npm install
```

## Usage

```bash
# Check entanglement between two files
node src/cli.js check --file1 path/to/file1.txt --file2 path/to/file2.txt

# Generate entanglement network for a directory
node src/cli.js network --dir path/to/directory --threshold 0.5

# Visualize entanglement graph
node src/cli.js visualize --graph data/entanglement.json
```

## Examples

```bash
# Check if your README and LICENSE are quantumly entangled
node src/cli.js check --file1 README.md --file2 LICENSE

# Find entangled files in your project
node src/cli.js network --dir src --threshold 0.3
```

## How It Works

The utility uses quantum-inspired algorithms to:

1. Analyze file content patterns and metadata
2. Calculate entanglement scores based on similarity and correlation
3. Generate quantum state representations
4. Provide insights into file relationships

## License

MIT
