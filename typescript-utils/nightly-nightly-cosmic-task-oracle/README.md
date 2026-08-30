# nightly-cosmic-task-oracle

A whimsical CLI tool that helps you decide your next task by consulting the cosmic alignments. No more decision paralysis! Just feed it your tasks, and the Cosmic Task Oracle will reveal which one holds the most cosmic energy for you to tackle right now.

## Features

- **Cosmic Prioritization**: Tasks are scored based on length, keywords, and a dash of cosmic randomness.
- **Type-Safe**: Built with TypeScript for robust and predictable behavior.
- **CLI Interface**: Easily integrate into your terminal workflow.

## Installation

1. Navigate to the `nightly-cosmic-task-oracle` directory.
2. Install dependencies:
   ```bash
   npm install
   ```

## Usage

You can provide tasks directly as command-line arguments or from a file.

### Via Command-Line Arguments

```bash
npm start "Fix critical bug in module X" "Refactor old API endpoint" "Dream up new feature for next sprint" "Write documentation for new CLI"
```

### Via a File

Create a `tasks.txt` file (or any `.txt` file) with one task per line:

```
# tasks.txt
Fix critical bug in module X
Refactor old API endpoint
Dream up new feature for next sprint
Write documentation for new CLI
Urgent: Review PR #123
```

Then run the oracle:

```bash
npm start -- --file tasks.txt
```

### Output

The oracle will output the task with the highest cosmic score, along with its score and the rationale.

```
✨ The Cosmic Task Oracle has spoken! ✨

Your next task, aligned with the cosmos, is:
------------------------------------------
Task: Dream up new feature for next sprint
Cosmic Score: 27.5
Rationale: High cosmic energy, contains 'dream' keyword, and aligned with the current moon phase.
------------------------------------------
May your efforts be cosmically productive!
```

## Development

To run tests:

```bash
npm test
```

## Contributing

Feel free to open issues or submit pull requests if you have ideas for new cosmic factors or improvements!
