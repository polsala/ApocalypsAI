# Nightly Quantum Entanglement Checker

A whimsical-yet-useful TypeScript CLI tool that detects quantum entanglement patterns in your code using simulated quantum states. Perfect for identifying tightly coupled components that might benefit from refactoring!

## Features

- 🎯 **Quantum State Simulation**: Uses simulated quantum mechanics to analyze code coupling
- 🔍 **Pattern Detection**: Identifies entangled code patterns that indicate tight coupling
- 📊 **Entanglement Score**: Provides a quantum-inspired score for code coupling
- 🛠️ **Type-Safe**: Built with TypeScript for robust development experience
- 📝 **Detailed Reports**: Generates comprehensive analysis reports

## Installation

```bash
npm install -g nightly-quantum-entanglement-checker
```

## Usage

```bash
# Analyze a TypeScript/JavaScript project
quantum-entangle-check ./src

# Generate detailed report
quantum-entangle-check ./src --report detailed

# Set custom entanglement threshold
quantum-entangle-check ./src --threshold 0.7

# Watch mode for development
quantum-entangle-check ./src --watch
```

## Output Example

```
🔬 Quantum Entanglement Analysis Report
=====================================

📁 Target: ./src
📅 Generated: 2024-01-15T10:30:00Z

📊 Overall Entanglement Score: 0.42 (Moderate)

⚠️  High Entanglement Detected:
   • user.service.ts ↔ auth.service.ts (Score: 0.87)
   • database.ts ↔ cache.ts (Score: 0.79)

💡 Recommendations:
   • Consider extracting shared dependencies
   • Implement dependency injection patterns
   • Review circular import chains

✅ Low entanglement detected in 85% of analyzed components
```

## API

### CLI Options

- `--report <type>`: Report type (simple|detailed|json)
- `--threshold <value>`: Entanglement threshold (0.0-1.0)
- `--watch`: Enable file watching mode
- `--help`: Show help information

### Programmatic Usage

```typescript
import { QuantumEntanglementAnalyzer } from 'nightly-quantum-entanglement-checker';

const analyzer = new QuantumEntanglementAnalyzer();
const result = await analyzer.analyze('./src', {
  threshold: 0.5,
  reportType: 'detailed'
});

console.log(result.entanglementScore);
console.log(result.entangledPairs);
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests: `npm test`
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Disclaimer

This tool uses simulated quantum mechanics for code analysis. While the entanglement metaphor is scientifically inspired, this is not a real quantum computing tool. Use it for fun and as a creative way to think about code coupling!
