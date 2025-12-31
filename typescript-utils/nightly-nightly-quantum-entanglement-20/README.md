# Nightly Quantum Entanglement Checker

A whimsical utility that checks if two pieces of code are 'quantum entangled' by comparing their structure and patterns. Perfect for finding duplicate logic, similar functions, or just having fun with code analysis!

## Features

- 🚀 Fast TypeScript implementation with Node.js
- 🔍 Deep structural code analysis
- 📊 Entanglement score calculation
- 🎭 Whimsical quantum-themed output
- 🧪 Comprehensive test suite
- 📝 Detailed README with examples

## Installation

```bash
npm install -g nightly-quantum-entanglement-checker
```

Or use directly with npx:

```bash
npx nightly-quantum-entanglement-checker file1.ts file2.ts
```

## Usage

### Command Line Interface

```bash
# Check entanglement between two files
quantum-entanglement file1.ts file2.ts

# Check entanglement with custom threshold
quantum-entanglement file1.ts file2.ts --threshold 0.8

# Output in JSON format
quantum-entanglement file1.ts file2.ts --json

# Verbose output with detailed analysis
quantum-entanglement file1.ts file2.ts --verbose
```

### Programmatic Usage

```typescript
import { QuantumEntanglementChecker } from './src/main';

const checker = new QuantumEntanglementChecker();

const result = await checker.checkEntanglement(
  'path/to/file1.ts',
  'path/to/file2.ts',
  { threshold: 0.75, verbose: true }
);

console.log(`Entanglement Score: ${result.score}`);
console.log(`Status: ${result.status}`);
```

## Examples

### Example 1: Similar Functions

```typescript
// file1.ts
function calculateTotal(items: number[]): number {
  return items.reduce((sum, item) => sum + item, 0);
}

// file2.ts
function sumArray(numbers: number[]): number {
  return numbers.reduce((acc, num) => acc + num, 0);
}
```

Output:
```
🔬 Quantum Entanglement Analysis
================================

File 1: file1.ts
File 2: file2.ts

Entanglement Score: 0.92 ⭐⭐⭐⭐⭐
Status: QUANTUM_ENTANGLED

Analysis:
- Structural similarity: 95%
- Function patterns: 90%
- Variable naming: 85%
- Logic flow: 95%

Conclusion: These functions are highly entangled!
```

### Example 2: Different Code

```typescript
// file1.ts
class UserManager {
  private users: User[] = [];
  
  addUser(user: User): void {
    this.users.push(user);
  }
}

// file2.ts
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
};
```

Output:
```
🔬 Quantum Entanglement Analysis
================================

File 1: file1.ts
File 2: file2.ts

Entanglement Score: 0.15 ⚪⚪⚪⚪⚪
Status: NO_ENTANGLEMENT

Analysis:
- Structural similarity: 20%
- Function patterns: 0%
- Variable naming: 10%
- Logic flow: 15%

Conclusion: No quantum entanglement detected.
```

## Configuration

### Options

- `--threshold <number>`: Minimum entanglement score to consider code entangled (default: 0.5)
- `--json`: Output results in JSON format
- `--verbose`: Show detailed analysis
- `--help`: Show help information

### Entanglement Status Levels

- **QUANTUM_ENTANGLED** (score ≥ 0.8): Highly similar code
- **PARTIALLY_ENTANGLED** (score ≥ 0.5): Moderately similar code
- **NO_ENTANGLEMENT** (score < 0.5): Different code

## Development

### Running Tests

```bash
npm test
```

### Building

```bash
npm run build
```

### Linting

```bash
npm run lint
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Quantum Disclaimer

This tool is for entertainment and code analysis purposes only. It does not actually measure quantum entanglement. Any resemblance to actual quantum physics is purely coincidental and whimsical.

## Support

If you encounter issues or have suggestions, please open an issue on our GitHub repository.

---

*May your code be ever entangled with good practices!*
