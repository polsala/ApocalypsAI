# Nightly Mood Task Oracle

## Summary
In the chaotic aftermath, decision fatigue can be a silent killer. The `nightly-mood-task-oracle` is a whimsical Node.js CLI utility designed to combat this by suggesting a slightly absurd, yet potentially productive, task based on your current mood or a random selection. Let the oracle guide your next step, however peculiar it may be.

## Installation

1.  Navigate to the `node-utils/nightly-mood-task-oracle` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Run the utility from the command line. You can specify a mood or let the oracle choose one for you.

### Options:

*   `--mood <mood_type>`: Specify your current mood. Available moods are `low-energy`, `medium-focus`, `high-chaos`, `creative-spark`.
*   `--random`: Let the oracle pick a mood and task completely at random.

### Examples:

*   **Get a task for a specific mood:**
    ```bash
    node src/index.js --mood low-energy
    # or, if installed globally via npm link:
    # mood-oracle --mood low-energy
    ```

*   **Get a completely random task:**
    ```bash
    node src/index.js --random
    # or:
    # mood-oracle --random
    ```

*   **If no options are provided, it defaults to a random mood/task:**
    ```bash
    node src/index.js
    # or:
    # mood-oracle
    ```

## Development & Testing

To run the automated tests:

```bash
npm test
```

Tests are deterministic and use mocks for `Math.random` to ensure consistent results.
