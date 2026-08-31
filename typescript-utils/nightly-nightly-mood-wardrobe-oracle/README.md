# Nightly Mood Wardrobe Oracle

## Overview

The `nightly-mood-wardrobe-oracle` is a whimsical-yet-useful utility that helps you select an outfit based on your current mood or desired vibe, rather than just the weather. It uses a type-safe system to define clothing items and moods, then suggests combinations that best match the chosen aesthetic and practical needs.

Ever feel like your clothes just don't match your inner 'Cozy Evening' or 'Edgy Rebel' spirit? This oracle is here to guide your sartorial choices!

## Features

*   **Mood-Based Suggestions**: Get outfit recommendations tailored to specific moods (e.g., 'Cozy Evening', 'Formal Business', 'Adventurous Explorer').
*   **Type-Safe Definitions**: Strong typing for clothing items (category, color, style, warmth) and moods ensures robust and predictable suggestions.
*   **Extensible Wardrobe**: Easily add your own clothing items and define new moods to personalize the experience.
*   **CLI Interface**: Simple command-line usage for quick outfit inspiration.

## Installation

1.  **Navigate to the utility directory:**
    ```bash
    cd typescript-utils/nightly-mood-wardrobe-oracle
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    # or
    yarn install
    ```

## Usage

To get an outfit suggestion, run the CLI tool with the desired mood name:

```bash
# Example: Get an outfit for a 'Cozy Evening'
npm run cli "Cozy Evening"

# Example: Get an outfit for 'Formal Business'
npm run cli "Formal Business"

# Example: Get an outfit for 'Adventurous Explorer'
npm run cli "Adventurous Explorer"

# Example: Get an outfit for 'Edgy Rebel'
npm run cli "Edgy Rebel"
```

If no mood is provided or the mood is not found, it will list available moods.

### Defining Your Own Wardrobe and Moods

You can modify `src/index.ts` to add your own `sampleWardrobe` items and `sampleMoods` definitions. Follow the `ClothingItem` and `Mood` interfaces defined in `src/types.ts`.

## Development

### Build

To compile the TypeScript code to JavaScript:

```bash
npm run build
```

### Run Tests

To execute the automated tests:

```bash
npm test
```

## Project Structure

```
nightly-mood-wardrobe-oracle/
├── README.md
├── package.json
├── tsconfig.json
├── jest.config.js
├── src/
│   ├── index.ts        # Main logic and CLI entry point
│   └── types.ts        # TypeScript interfaces for ClothingItem and Mood
└── tests/
    └── index.test.ts   # Unit tests for outfit suggestion logic
```
