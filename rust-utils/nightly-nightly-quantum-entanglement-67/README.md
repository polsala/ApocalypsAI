# Nightly Quantum Entanglement Checker

A whimsical-yet-useful Rust CLI tool that simulates quantum entanglement verification for distributed systems using Bell's inequality tests. Perfect for testing distributed system reliability and adding some quantum flair to your workflow.

## Features

- Simulates quantum entanglement verification using Bell's inequality
- Generates entanglement reports with statistical analysis
- Supports both local and distributed entanglement testing
- Whimsical quantum-themed output with ASCII art
- Fast, memory-efficient Rust implementation

## Installation

### From Source

```bash
# Clone the repository
git clone <repo-url>
cd utils/nightly-quantum-entanglement-checker

# Build the project
cargo build --release

# Install to PATH
cargo install --path .
```

### Usage

```bash
# Basic entanglement check
nightly-quantum-entanglement-checker check

# Generate entanglement report
nightly-quantum-entanglement-checker report --samples 1000

# Distributed entanglement test
nightly-quantum-entanglement-checker distributed --nodes 5 --rounds 100

# Help
nightly-quantum-entanglement-checker --help
```

## Commands

- `check`: Perform a basic entanglement verification
- `report`: Generate detailed entanglement statistics
- `distributed`: Test entanglement across multiple simulated nodes
- `help`: Show help information

## Output Example

```
🔬 Quantum Entanglement Verification Report
=========================================

Entanglement Status: ✅ VERIFIED
Bell Inequality Violation: 2.718
Statistical Significance: 99.7%

Quantum Correlation Matrix:
[████████████████████] 100% entangled

Recommendation: Your system exhibits strong quantum correlations!
```

## Technical Details

This tool simulates quantum entanglement using:
- Bell's inequality calculations
- Monte Carlo simulation methods
- Statistical hypothesis testing
- Random number generation with quantum-inspired seeding

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please follow standard Rust conventions and include tests for new features.
