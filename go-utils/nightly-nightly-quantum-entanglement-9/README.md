# Nightly Quantum Entanglement Checker

A whimsical-yet-useful Go utility that simulates quantum entanglement verification for distributed systems. Uses concurrent goroutines and channels to demonstrate Go's powerful concurrency model.

## Features

- Simulates quantum particle pairs and their entanglement states
- Concurrent verification using goroutines and channels
- Configurable particle count and verification timeout
- ASCII art visualization of entanglement states
- Educational tool for learning Go concurrency patterns

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd <repo-url>/go-utils/nightly-quantum-entanglement-checker

# Build the utility
go build -o entanglement-checker ./src

# Run the utility
./entanglement-checker --particles=100 --timeout=5
```

## Usage

```bash
./entanglement-checker [flags]

Flags:
  -p, --particles int    Number of particle pairs to simulate (default 50)
  -t, --timeout int      Verification timeout in seconds (default 3)
  -v, --verbose          Enable verbose output
  -h, --help             Show help
```

## Example Output

```
🔬 Initializing Quantum Entanglement Checker...

Creating 50 entangled particle pairs...

📡 Verifying entanglement states...

Particle Pair 1: ✓ Entangled
Particle Pair 2: ✓ Entangled
Particle Pair 3: ✓ Entangled
...

🎉 All 50 particle pairs verified successfully!

Entanglement verification complete in 2.3s
```

## Educational Value

This utility demonstrates:

- Goroutine creation and management
- Channel communication patterns
- Select statements for timeout handling
- Concurrent data processing
- Struct embedding and interfaces

Perfect for learning Go concurrency concepts!

## License

MIT
