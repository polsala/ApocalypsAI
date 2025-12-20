# Nightly Quantum Quip Generator

A whimsical utility that generates quantum computing jokes and explanations for developers. Perfect for breaking the ice at tech meetups or adding some quantum humor to your documentation.

## Features

- Generates quantum computing jokes
- Provides explanations for non-quantum developers
- CLI interface with multiple output formats
- Configurable joke categories
- Interactive mode for live joke generation

## Installation

```bash
npm install -g nightly-quantum-quip-generator
```

## Usage

### Command Line Interface

```bash
# Generate a random quantum joke
quantum-quip

# Generate a joke with explanation
quantum-quip --explain

# Generate a specific category of joke
quantum-quip --category superposition

# List available categories
quantum-quip --list-categories

# Interactive mode
quantum-quip --interactive

# Output as JSON
quantum-quip --format json
```

### Programmatic Usage

```javascript
const { QuantumQuipGenerator } = require('nightly-quantum-quip-generator');

const generator = new QuantumQuipGenerator();

// Generate a random joke
const joke = generator.generateJoke();
console.log(joke.text);

// Generate with explanation
const explainedJoke = generator.generateJoke({ explain: true });
console.log(explainedJoke.text);
console.log(explainedJoke.explanation);

// Generate from specific category
const categoryJoke = generator.generateJoke({ category: 'entanglement' });
console.log(categoryJoke.text);
```

## Categories

- **superposition**: Jokes about things being in multiple states
- **entanglement**: Jokes about spooky action at a distance
- **qubits**: Jokes specifically about quantum bits
- **algorithms**: Jokes about quantum algorithms
- **hardware**: Jokes about quantum hardware
- **general**: General quantum computing humor

## Output Formats

- **text**: Plain text output (default)
- **json**: Structured JSON output
- **markdown**: Markdown formatted output

## Examples

```bash
$ quantum-quip
Why don't quantum programmers ever make mistakes?
Because they exist in a superposition of correct and incorrect until observed!

$ quantum-quip --explain
Why don't quantum programmers ever make mistakes?
Because they exist in a superposition of correct and incorrect until observed!

Explanation: In quantum mechanics, particles can exist in multiple states simultaneously until measured. Similarly, quantum programmers might argue their code is both correct and incorrect until someone actually runs it!

$ quantum-quip --category entanglement --format json
{
  "text": "Why are quantum particles terrible gossips?\nBecause once they're entangled, they always know what the other is up to!",
  "category": "entanglement",
  "explanation": "Quantum entanglement is a phenomenon where particles become linked and instantly affect each other regardless of distance. It's like having a quantum-level group chat!"
}
```

## License

MIT License - feel free to use these jokes in your presentations (with attribution appreciated but not required).

## Contributing

Add new jokes to the `src/jokes.js` file following the existing format. Make sure to:

1. Include a category
2. Provide a clear explanation
3. Keep it family-friendly
4. Test your additions with the test suite

## Acknowledgments

Inspired by the wonderful world of quantum computing and the brave developers trying to understand it!
