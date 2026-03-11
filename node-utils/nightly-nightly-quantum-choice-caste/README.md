# Nightly Quantum Choice Caster

## 🌌 Embrace the Cosmic Flow of Decision-Making 🌌

The `nightly-quantum-choice-caster` is a whimsical command-line utility designed to help you overcome decision paralysis by consulting the 'void' for a random, yet cosmically guided, choice. Provide it with a list of options, and it will 'quantum cast' one for you, accompanied by a delightful message from the beyond.

Whether you're deciding between scavenging routes, repair priorities, or simply what to have for your next meal in the post-apocalyptic landscape, let the Quantum Choice Caster illuminate your path.

## Installation

1.  **Navigate to the utility directory:**
    ```bash
    cd node-utils/nightly-quantum-choice-caster
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Make the CLI tool executable (optional, but recommended for global use):**
    ```bash
    npm link
    ```
    Or, run directly using `node src/index.js`.

## Usage

Simply provide your options as arguments to the command. Enclose options with spaces in quotes.

```bash
nightly-quantum-choice-caster "Explore Sector 7" "Fortify the Bunker" "Seek out the Elder Scrolls" "Brew more mushroom tea"
```

### Example Output

```

Ripples of possibility coalesce, and the universe points to...

✨ Fortify the Bunker ✨

May your choice lead to optimal temporal stability.
```

### No Options Provided

If you run the command without any options, it will display a usage message:

```bash
nightly-quantum-choice-caster
```

```
🌌 ApocalypsAI Quantum Choice Caster 🌌
Usage: nightly-quantum-choice-caster <option1> <option2> [option3...]

Example: nightly-quantum-choice-caster "Explore the ruins" "Scavenge for supplies" "Rest and repair"
```

## Development & Testing

To run the automated tests for this utility:

```bash
npm test
```

Tests are deterministic and use mocks for `Math.random`, `console.log`, and `process.exit` to ensure consistent results without side effects.
