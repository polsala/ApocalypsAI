# Nightly Quantum Entanglement Checker

A whimsical utility that checks if two code snippets are 'quantum entangled' by comparing their hash signatures with a touch of chaos theory.

## Features
- 🚀 Fast TypeScript implementation
- 🔗 Compares code snippets using quantum-inspired hash algorithms
- 🎲 Adds a touch of chaos theory for fun
- 📊 Provides entanglement probability scores
- 🧪 Includes comprehensive tests

## Installation

```bash
npm install -g nightly-quantum-entanglement-checker
```

## Usage

```typescript
import { QuantumEntanglementChecker } from './src/main';

const checker = new QuantumEntanglementChecker();

const code1 = `function hello() { console.log('Hello World'); }`;
const code2 = `function hello() { console.log('Hello World'); }`;

const result = checker.checkEntanglement(code1, code2);
console.log(`Entanglement Score: ${result.score}`);
console.log(`Are Entangled: ${result.entangled}`);
```

## CLI Usage

```bash
npx nightly-quantum-entanglement-checker --file1 code1.ts --file2 code2.ts
```

## License
MIT
