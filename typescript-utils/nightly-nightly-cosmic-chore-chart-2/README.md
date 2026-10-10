# Nightly Cosmic Chore Chart

## Overview

The `nightly-cosmic-chore-chart` is a whimsical utility designed to inject a bit of cosmic randomness and fun into your daily chore assignments. In the chaotic post-apocalyptic world, maintaining routine can be a challenge. This tool helps by generating a daily chore list, influenced by a 'cosmic energy' that might boost or hinder certain tasks.

It's a type-safe command-line tool built with TypeScript, ensuring robust data handling for your vital daily tasks.

## Features

*   **Cosmic Influence:** Each day, a unique 'cosmic energy' is generated, affecting chore difficulty and providing a fun narrative.
*   **Configurable Chores:** Define your own list of chores, their base difficulty, and tags in a simple JSON file.
*   **Intelligent Assignment:** Selects a specified number of chores, taking into account cosmic boosts and hindrances.
*   **Type-Safe:** Built with TypeScript for reliability and maintainability.

## Installation

To use this utility, you'll need Node.js and npm (or yarn) installed.

1.  Clone the repository or download the utility files:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-cosmic-chore-chart
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  You can then run it directly or build it:
    ```bash
    npm run build
    # To run directly:
    # npx ts-node src/index.ts --chores-file chores.json --num-chores 3
    # Or after building:
    # node dist/index.js --chores-file chores.json --num-chores 3
    ```

## Usage

First, create a `chores.json` file (or similar) defining your available chores. See the example below.

```bash
node dist/index.js --chores-file <path-to-your-chores.json> --num-chores <number-of-chores-to-assign>
```

**Arguments:**

*   `--chores-file <path>`: (Required) Path to your JSON file containing the list of chores.
*   `--num-chores <number>`: (Optional) The number of chores to assign. Defaults to 3.

## Example `chores.json`

```json
[
  {
    "id": "c1",
    "name": "Scavenge for Water",
    "baseDifficulty": 4,
    "tags": ["survival", "physical", "outdoor"]
  },
  {
    "id": "c2",
    "name": "Repair Shelter Wall",
    "baseDifficulty": 3,
    "tags": ["maintenance", "physical"]
  },
  {
    "id": "c3",
    "name": "Inventory Supplies",
    "baseDifficulty": 2,
    "tags": ["logistics", "mental"]
  },
  {
    "id": "c4",
    "name": "Clean Contamination Zone",
    "baseDifficulty": 5,
    "tags": ["danger", "physical", "hygiene"]
  },
  {
    "id": "c5",
    "name": "Tend to Hydroponics",
    "baseDifficulty": 3,
    "tags": ["farming", "maintenance"]
  },
  {
    "id": "c6",
    "name": "Sharpen Tools",
    "baseDifficulty": 1,
    "tags": ["maintenance", "crafting"]
  },
  {
    "id": "c7",
    "name": "Monitor Perimeter Sensors",
    "baseDifficulty": 2,
    "tags": ["security", "mental"]
  }
]
```

## Example Output

```
🌌 Nightly Cosmic Chore Chart 🌌

Today's Cosmic Influence: Void Whisper (Difficulty Modifier: 0.8)
Favored Tags: [mental, logistics]
Hindered Tags: [physical, danger]
Cosmic Message: "The void whispers secrets of efficiency. Focus your mind, not your muscle."

--- Your Assigned Chores ---

1. Inventory Supplies (Effective Difficulty: 1.6) - ✨ Cosmic Boost!
2. Monitor Perimeter Sensors (Effective Difficulty: 1.6) - ✨ Cosmic Boost!
3. Tend to Hydroponics (Effective Difficulty: 2.4)

May your cosmic endeavors be fruitful!
```

## Development

To run tests:

```bash
npm test
```
