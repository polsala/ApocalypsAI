# Nightly Scavenged Blueprint Checker

## Overview

In the desolate wastes, every scavenged component counts. The `nightly-scavenged-blueprint-checker` is a type-safe TypeScript utility designed to help survivors (or their automated assistants) determine if they possess all the necessary components, in sufficient quantities, to craft a specific blueprint. No more wasted effort attempting to build a "Temporal Flux Capacitor" only to realize you're short on "Glimmering Shards"!

This tool provides clear feedback on what can be crafted and, crucially, what components are still missing and in what quantities.

## Features

*   **Type-Safe:** Leverages TypeScript interfaces for `Component`, `BlueprintRequirement`, `Blueprint`, and `Inventory` to ensure robust and predictable data handling.
*   **Clear Validation:** Returns a boolean indicating craftability and a detailed list of any missing components.
*   **Whimsical & Useful:** Helps manage post-apocalyptic crafting resources with a touch of thematic flair.

## Installation

To use this utility, you'll need Node.js and npm (or yarn) installed.

1.  Navigate to the utility's directory:
    ```bash
    cd typescript-utils/nightly-scavenged-blueprint-checker
    ```
2.  Install dependencies:
    ```bash
    npm install
    # or yarn install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## Usage

Import the `checkBlueprint` function and relevant types into your TypeScript or JavaScript project.

### Example

Let's say you have an inventory of scavenged items and a blueprint for a "Void-Resonating Communicator".

```typescript
// my-survival-script.ts
import { checkBlueprint, Inventory, Blueprint, Component } from './dist/index';

// 1. Define your current inventory
const myInventory: Inventory = new Map([
  ["Rusty Cog", 5],
  ["Glimmering Shard", 2],
  ["Whisper-Infused Wire", 10],
  ["Scrap Metal", 50]
]);

// 2. Define a blueprint you want to check
const voidCommunicatorBlueprint: Blueprint = {
  name: "Void-Resonating Communicator",
  requirements: [
    { componentName: "Rusty Cog", requiredQuantity: 3 },
    { componentName: "Glimmering Shard", requiredQuantity: 1 },
    { componentName: "Temporal Flux Capacitor", requiredQuantity: 1 } // This one is missing!
  ],
};

const basicSurvivalKitBlueprint: Blueprint = {
  name: "Basic Survival Kit",
  requirements: [
    { componentName: "Scrap Metal", requiredQuantity: 20 },
    { componentName: "Whisper-Infused Wire", requiredQuantity: 5 }
  ],
};

// 3. Check the blueprints against your inventory
console.log(`--- Checking: ${voidCommunicatorBlueprint.name} ---`);
const resultVoidComm = checkBlueprint(myInventory, voidCommunicatorBlueprint);
console.log(`Can craft: ${resultVoidComm.canCraft}`);
if (!resultVoidComm.canCraft) {
  console.log("Missing components:");
  resultVoidComm.missingComponents.forEach(mc => {
    console.log(`  - ${mc.name}: ${mc.quantity} more needed`);
  });
}

console.log(`\n--- Checking: ${basicSurvivalKitBlueprint.name} ---`);
const resultSurvivalKit = checkBlueprint(myInventory, basicSurvivalKitBlueprint);
console.log(`Can craft: ${resultSurvivalKit.canCraft}`);
if (!resultSurvivalKit.canCraft) {
  console.log("Missing components:");
  resultSurvivalKit.missingComponents.forEach(mc => {
    console.log(`  - ${mc.name}: ${mc.quantity} more needed`);
  });
}
```

### Expected Output for the example above:

```
--- Checking: Void-Resonating Communicator ---
Can craft: false
Missing components:
  - Temporal Flux Capacitor: 1 more needed

--- Checking: Basic Survival Kit ---
Can craft: true
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

This will compile the TypeScript files from `src/` into JavaScript in the `dist/` directory, along with their type definitions.
