# Nightly Cosmic Whisper Oracle

## Overview

The `nightly-cosmic-whisper-oracle` is a whimsical-yet-useful command-line interface (CLI) tool designed to help you make decisions in the uncertain world of the post-apocalypse. When decision fatigue sets in, or you simply need a fresh perspective, consult the 'Cosmic Whispers' for structured advice on various aspects of survival.

This utility is built with TypeScript, ensuring type safety and a robust structure for its generated advice.

## Features

*   **Whimsical Advice**: Generates unique, themed prompts for action.
*   **Categorized Guidance**: Get advice tailored to specific areas like Resource, Shelter, Social, Exploration, Self-Care, or a Wildcard.
*   **Risk Assessment**: Each whisper comes with an associated risk level.
*   **Type-Safe**: Built with TypeScript for reliability and maintainability.

## Installation

To use this utility, you need Node.js and npm (or yarn) installed on your system.

1.  **Navigate to the utility directory:**
    ```bash
    cd nightly-cosmic-whisper-oracle
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    # or yarn install
    ```
3.  **Build the TypeScript project:**
    ```bash
    npm run build
    ```
4.  **Link the CLI tool (optional, for global access):**
    ```bash
    npm link
    # or yarn link
    ```
    If you don't link it globally, you can run it using `node dist/cli.js` from the utility's root directory.

## Usage

Run the `cosmic-whisper` command from your terminal. You can optionally specify a category to narrow down the advice.

```bash
# Get a random whisper from any category
cosmic-whisper

# Get a whisper specifically about 'Resource' management
cosmic-whisper Resource

# Get a whisper about 'Shelter' maintenance
cosmic-whisper Shelter

# Get a whisper about 'Social' interactions
cosmic-whisper Social

# Get a whisper about 'Exploration'
cosmic-whisper Exploration

# Get a whisper about 'Self-Care'
cosmic-whisper Self-Care

# Get a truly unpredictable 'Wildcard' whisper
cosmic-whisper Wildcard
```

### Example Output

```
--- Cosmic Whisper Oracle ---

Category: Resource
Prompt: Seek the shimmering dew-drops beneath the rusted bridge.
Action: Scavenge
Risk Level: Low
Timestamp: 4/23/2024, 10:30:00 AM

-----------------------------
```

## Development

### Running Tests

```bash
npm test
# or yarn test
```

### Building the Project

```bash
npm run build
# or yarn build
```

This will compile the TypeScript files from `src/` into JavaScript in the `dist/` directory.
