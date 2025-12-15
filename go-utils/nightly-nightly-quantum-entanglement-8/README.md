# Nightly Quantum Entanglement Checker

A whimsical-yet-useful Go utility that generates and verifies quantum entanglement simulations for distributed systems. Perfect for testing distributed consensus algorithms, blockchain networks, and quantum-inspired architectures!

## Features

- 🚀 Generate quantum entanglement pairs with configurable fidelity
- 🔗 Verify entanglement across distributed nodes
- 📊 Monitor quantum state coherence over time
- 🎲 Simulate quantum decoherence and measurement collapse
- 🌐 REST API for integration with existing systems
- 🧪 Comprehensive test suite with deterministic mocks

## Installation

```bash
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/go-utils/nightly-quantum-entanglement-checker

# Build the binary
go build -o qentangle ./cmd/qentangle

# Run the server
go run ./cmd/qentangle server --port 8080
```

## Usage

### Command Line Interface

```bash
# Generate entangled pairs
./qentangle generate --pairs 10 --fidelity 0.95

# Verify entanglement
./qentangle verify --node-a node1 --node-b node2 --pairs 5

# Monitor coherence
./qentangle monitor --duration 30s --threshold 0.8
```

### REST API

```bash
# Generate pairs via HTTP
curl -X POST http://localhost:8080/api/v1/entangle \n  -H "Content-Type: application/json" \n  -d '{"pairs": 5, "fidelity": 0.92}'

# Verify entanglement
curl -X GET http://localhost:8080/api/v1/verify?nodeA=node1&nodeB=node2

# Get coherence status
curl http://localhost:8080/api/v1/coherence
```

## Configuration

Create a `config.yaml` file:

```yaml
server:
  port: 8080
  host: 0.0.0.0
quantum:
  default_fidelity: 0.95
  decoherence_rate: 0.01
  measurement_threshold: 0.8
logging:
  level: info
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/quantum-improvements`
3. Commit your changes: `git commit -m 'Add quantum improvements'`
4. Push to the branch: `git push origin feature/quantum-improvements`
5. Open a Pull Request

## License

MIT License - see LICENSE file for details.

## Disclaimer

This is a simulation tool for educational and testing purposes. It does not create actual quantum entanglement.
