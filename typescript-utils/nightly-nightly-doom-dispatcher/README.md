# Nightly Doom Dispatcher

A whimsical command-line utility for the ApocalypsAI community that helps you prioritize your daily tasks by assigning them a "Doom Level" and a "Whimsy Bonus." Because even in the apocalypse, a little humor and a clear (if comically grim) priority list can make all the difference.

## Features

*   **Doom Level Assignment**: Each task is randomly assigned a severity, from "Minor Glitch" to "Existential Threat."
*   **Whimsy Bonus**: A touch of lightheartedness is added with a "Whimsy Bonus," ranging from "Faint Sparkle" to "Cosmic Joke."
*   **Prioritization**: Tasks are sorted based on a combined score, allowing you to tackle the most "doomed" (or whimsically challenging) items first.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.

## Installation

1.  Ensure you have Node.js and npm (or yarn) installed.
2.  Navigate to the `typescript-utils/nightly-doom-dispatcher` directory.
3.  Install dependencies:
    ```bash
    npm install
    # or yarn install
    ```
4.  Build the TypeScript project:
    ```bash
    npm run build
    # or yarn build
    ```

## Usage

Run the dispatcher with your tasks as arguments:

```bash
node dist/index.js "Fix the temporal anomaly" "Feed the void-cat" "Debug the reality distortion field" "Water the mutant cacti"
```

Or pipe tasks from a file (one task per line):

```bash
cat tasks.txt | node dist/index.js
```

Example `tasks.txt`:
```
Fix the temporal anomaly
Feed the void-cat
Debug the reality distortion field
Water the mutant cacti
Calibrate the chronometer
```

### Output Example

```
--- Daily Doom Dispatch ---

1. [Existential Threat + Cosmic Joke] Debug the reality distortion field
2. [Impending Catastrophe + Gentle Giggle] Fix the temporal anomaly
3. [Impending Catastrophe + Faint Sparkle] Calibrate the chronometer
4. [Minor Glitch + Cosmic Joke] Feed the void-cat
5. [Minor Glitch + Gentle Giggle] Water the mutant cacti

May your efforts avert total annihilation... or at least make it amusing.
```

## Development

To run tests:

```bash
npm test
# or yarn test
```
