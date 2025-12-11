## Nightly Quantum Entanglement Checker

A whimsical-yet-useful Go utility that simulates quantum entanglement verification for distributed systems. Perfect for testing distributed consensus algorithms, network reliability, and adding some quantum flavor to your infrastructure!

### Features
- Simulates quantum entanglement verification between nodes
- Generates quantum state reports with spooky action at a distance metrics
- Includes entanglement fidelity scoring
- Whimsical quantum-themed output
- Concurrent verification using Go's goroutines

### Usage
```bash
# Build the utility
go build -o quantum-entanglement-checker

# Run with default settings
./quantum-entanglement-checker

# Run with custom nodes
./quantum-entanglement-checker --nodes node1,node2,node3

# Run with verbose quantum state reporting
./quantum-entanglement-checker --verbose
```

### Example Output
```
🔬 Initializing Quantum Entanglement Checker...

📡 Establishing quantum links between 3 nodes...

✨ Quantum Entanglement Report:

Node A (node1) ↔ Node B (node2)
  • Entanglement Fidelity: 98.7%
  • Spooky Action Score: 9.2/10
  • Quantum State: ✅ CORRELATED
  • Bell Inequality: VIOLATED (as expected!)

Node A (node1) ↔ Node C (node3)
  • Entanglement Fidelity: 96.3%
  • Spooky Action Score: 8.7/10
  • Quantum State: ✅ CORRELATED
  • Bell Inequality: VIOLATED (as expected!)

Node B (node2) ↔ Node C (node3)
  • Entanglement Fidelity: 99.1%
  • Spooky Action Score: 9.5/10
  • Quantum State: ✅ CORRELATED
  • Bell Inequality: VIOLATED (as expected!)

🎉 Overall System Entanglement: 98.0% (EXCELLENT)

🔮 Quantum Recommendation: Your distributed system exhibits strong quantum correlations!
```

### Installation
```bash
go install github.com/polsala/ApocalypsAI/go-utils/nightly-quantum-entanglement-checker@latest
```
