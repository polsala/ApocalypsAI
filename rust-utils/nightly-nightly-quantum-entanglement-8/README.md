# Nightly Quantum Entanglement Checker

A whimsical CLI tool that checks if two code snippets are 'quantum entangled' by comparing their structure and content in a fun, probabilistic way.

## Features

- **Quantum Metaphor**: Uses quantum physics terminology to describe code similarity
- **Probabilistic Matching**: Returns a 'quantum probability' score
- **Multi-language Support**: Works with various programming languages
- **Entanglement States**: Categorizes matches as 'superposed', 'collapsed', or 'decohered'
- **CLI Interface**: Simple command-line tool with colorful output

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd <repo-url>

# Build the tool
cargo build --release

# Or install directly
cargo install --path .
```

## Usage

```bash
# Compare two files
quantum-entanglement-checker file1.rs file2.rs

# Compare with custom threshold
quantum-entanglement-checker --threshold 0.8 file1.rs file2.rs

# Verbose output with quantum state details
quantum-entanglement-checker --verbose file1.rs file2.rs

# Compare specific functions
quantum-entanglement-checker --function "calculate" file1.rs file2.rs
```

## Example Output

```
🔬 Quantum Entanglement Analysis
================================

File A: src/lib.rs
File B: src/utils.rs

Entanglement Probability: 73.4%
Quantum State: Superposed

Particle Correlation: 0.68
Wave Function Overlap: 0.75
Decoherence Factor: 0.12

Conclusion: The code exhibits moderate quantum entanglement.
Recommendation: Observe with caution - collapse may occur during runtime.
```

## Quantum States Explained

- **Superposed**: Code shows potential similarity but needs observation
- **Collapsed**: Clear similarity detected with high confidence
- **Decohered**: No meaningful entanglement found

## License

MIT License - feel free to use in your quantum computing projects!
