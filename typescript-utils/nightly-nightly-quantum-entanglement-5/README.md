# Nightly Quantum Entanglement Checker

A whimsical-yet-useful utility that simulates quantum entanglement verification for distributed systems. Perfect for testing spooky action at a distance in your codebase!

## Features

- Simulates quantum entanglement between distributed nodes
- Provides spooky correlation metrics
- Generates quantum-safe random numbers
- Includes comprehensive test suite

## Installation

```bash
npm install nightly-quantum-entanglement-checker
```

## Usage

```typescript
import { QuantumEntanglementChecker } from './src/main';

const checker = new QuantumEntanglementChecker();

// Create entangled particles
const particleA = checker.createEntangledParticle('node-a');
const particleB = checker.createEntangledParticle('node-b');

// Measure particles
const resultA = checker.measureParticle(particleA, 'spin');
const resultB = checker.measureParticle(particleB, 'spin');

console.log(`Particle A: ${resultA}`);
console.log(`Particle B: ${resultB}`);
console.log(`Entangled correlation: ${checker.getCorrelation(particleA, particleB)}`);
```

## API

### `QuantumEntanglementChecker`

#### `createEntangledParticle(nodeId: string): EntangledParticle`
Creates a new entangled particle for the specified node.

#### `measureParticle(particle: EntangledParticle, property: string): QuantumMeasurement`
Measures a quantum property of the particle.

#### `getCorrelation(particleA: EntangledParticle, particleB: EntangledParticle): number`
Returns the correlation coefficient between two entangled particles.

#### `verifyEntanglement(particleA: EntangledParticle, particleB: EntangledParticle): boolean`
Verifies if two particles are still entangled.

## License

MIT
