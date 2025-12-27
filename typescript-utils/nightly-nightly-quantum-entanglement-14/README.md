# Nightly Quantum Entanglement Tracker

A whimsical TypeScript utility that simulates quantum entanglement states for fun and educational purposes. Perfect for understanding quantum mechanics concepts or just adding some quantum flair to your projects!

## Features

- Simulates quantum entanglement between particles
- Visualizes entanglement states with ASCII art
- Educational tool for quantum mechanics concepts
- Command-line interface for interactive exploration
- TypeScript implementation with full type safety

## Installation

```bash
npm install nightly-quantum-entanglement-tracker
```

## Usage

### CLI Interface

```bash
# Start the quantum entanglement simulator
npx nightly-quantum-entanglement-tracker

# View help
npx nightly-quantum-entanglement-tracker --help

# Simulate specific entanglement states
npx nightly-quantum-entanglement-tracker --particles 4 --duration 10
```

### Programmatic Usage

```typescript
import { QuantumEntanglementSimulator } from './src/main';

const simulator = new QuantumEntanglementSimulator({
  particleCount: 3,
  simulationDuration: 5
});

// Start simulation
simulator.start();

// Get current state
const currentState = simulator.getCurrentState();
console.log('Current entanglement state:', currentState);

// Observe particles (collapses superposition)
const observation = simulator.observe();
console.log('Observation result:', observation);
```

## Examples

### Basic Simulation

```typescript
import { QuantumEntanglementSimulator } from './src/main';

const simulator = new QuantumEntanglementSimulator({
  particleCount: 2,
  simulationDuration: 3
});

simulator.on('stateChange', (state) => {
  console.log('Entanglement state updated:', state);
});

simulator.on('observation', (result) => {
  console.log('Particle observed:', result);
});

simulator.start();
```

### Advanced Configuration

```typescript
const simulator = new QuantumEntanglementSimulator({
  particleCount: 5,
  simulationDuration: 10,
  decoherenceRate: 0.1,
  entanglementStrength: 0.8
});

// Listen for quantum events
simulator.on('decoherence', (details) => {
  console.log('Quantum decoherence detected:', details);
});

simulator.on('entanglementBreak', (details) => {
  console.log('Entanglement broken:', details);
});

simulator.start();
```

## API Reference

### QuantumEntanglementSimulator

Main class for simulating quantum entanglement.

#### Constructor

```typescript
new QuantumEntanglementSimulator(options: SimulationOptions)
```

#### Options

- `particleCount`: Number of particles to simulate (default: 2)
- `simulationDuration`: Duration in seconds (default: 5)
- `decoherenceRate`: Rate of quantum decoherence (default: 0.05)
- `entanglementStrength`: Initial entanglement strength (default: 0.9)

#### Methods

- `start()`: Start the simulation
- `stop()`: Stop the simulation
- `getCurrentState()`: Get current entanglement state
- `observe()`: Observe particles (collapses superposition)
- `reset()`: Reset simulation to initial state

#### Events

- `stateChange`: Emitted when entanglement state changes
- `observation`: Emitted when particles are observed
- `decoherence`: Emitted when quantum decoherence occurs
- `entanglementBreak`: Emitted when entanglement breaks

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please follow standard TypeScript practices and include tests for new features.

## Disclaimer

This is a whimsical educational tool and not a scientifically accurate quantum physics simulator. Use it for fun and learning, not for actual quantum computing!
