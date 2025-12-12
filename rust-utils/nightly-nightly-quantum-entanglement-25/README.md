# Nightly Quantum Entanglement Checker

A whimsical-yet-useful utility that simulates quantum entanglement verification for distributed systems. Perfect for testing distributed consensus algorithms or just adding some quantum flavor to your infrastructure!

## Features

- Simulates quantum entanglement between nodes
- Verifies quantum state consistency across distributed systems
- Provides whimsical quantum-themed status messages
- Uses Rust's async/await for efficient concurrent operations

## Installation

```bash
# Clone the repository
git clone <repo-url>

# Navigate to the utility directory
cd rust-utils/nightly-quantum-entanglement-checker

# Build the project
cargo build --release
```

## Usage

```bash
# Run with default settings
cargo run --release

# Run with custom number of nodes
cargo run --release -- --nodes 8

# Run with verbose quantum state output
cargo run --release -- --verbose
```

## Example Output

```
🔬 Initializing quantum entanglement checker...

⚛️  Entangling 4 nodes...
✓ Node 0: Quantum state |0⟩
✓ Node 1: Quantum state |1⟩
✓ Node 2: Quantum state |+⟩
✓ Node 3: Quantum state |-⟩

🌀 Verifying quantum entanglement...
✓ Quantum coherence verified across all nodes
✓ Bell state measurements: 0.998
✓ No spooky action at a distance detected

🎉 All nodes are quantumly entangled!
```

## Testing

```bash
# Run all tests
cargo test

# Run with verbose output
cargo test -- --nocapture
```

## License

MIT License - see LICENSE file for details.
