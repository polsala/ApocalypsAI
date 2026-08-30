# Nightly Cosmic Chore Chart

## Overview

The `nightly-cosmic-chore-chart` is a whimsical command-line utility that generates a daily list of chores, each influenced by a unique "cosmic alignment" for the day. It aims to bring a touch of playful magic to mundane tasks, offering a fresh perspective on daily responsibilities.

Each day, based on a deterministic cosmic cycle, a different celestial influence (e.g., Lunar Lull, Martian Momentum) guides the selection and description of your suggested tasks, making your chore routine an adventure through the cosmos.

## Features

*   **Cosmic Guidance**: Daily chores are themed and suggested based on a rotating cosmic influence.
*   **Whimsical Descriptions**: Each chore comes with a lighthearted, space-themed description.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.
*   **CLI Interface**: Easy to run from your terminal to get your daily cosmic tasks.

## Installation

To use this utility, you need Node.js and npm (or yarn) installed on your system.

1.  Navigate to the `typescript-utils/nightly-cosmic-chore-chart` directory.
2.  Install the dependencies:

    ```bash
    npm install
    # or yarn install
    ```

## Usage

After installation, you can build and run the utility:

1.  Build the TypeScript code:

    ```bash
    npm run build
    ```

2.  Run the utility to get your daily cosmic chore chart:

    ```bash
    npm start
    ```

    Example Output:
    ```
    --- Nightly Cosmic Chore Chart for Mon, Apr 29, 2024 ---
    Cosmic Influence: LunarLull
    Guidance: The moon whispers secrets of gentle tidiness. Focus on quiet, reflective tasks.

    Your Cosmic Tasks:
      1. [Daily] Dust the cosmic shelves (Effort: low)
      2. [Daily] Sweep away astral dust bunnies (Effort: low)
      3. [Self-Care] Meditate on the void (Effort: low)
      4. [Self-Care] Align your chakras with the constellations (Effort: medium)
      5. [Daily] Water the space succulents (Effort: low)

    May your efforts align with the stars!
    ```

## Development

### Running Tests

To ensure everything is working as expected, run the automated tests:

```bash
npm test
```

### Project Structure

```
.gitignore
package.json
tsconfig.json
jest.config.js
README.md
src/
  index.ts
  cosmicChoreGenerator.ts
  types.ts
tests/
  cosmicChoreGenerator.test.ts
```
