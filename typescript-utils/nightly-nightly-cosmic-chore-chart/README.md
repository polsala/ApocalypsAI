# Nightly Cosmic Chore Chart

The ApocalypsAI Nightly Integrator presents the "Nightly Cosmic Chore Chart" – a whimsical yet essential utility for prioritizing your nightly (or daily) tasks based on the ever-shifting cosmic energies and their apocalyptic implications. Never again wonder if you should "Recalibrate Chrono-Synthesizer" before "Inventory Ration Supplies" when the Lunar Alignment is peaking and Void Whispers are intense!

This utility allows you to define tasks with base priorities and specific sensitivities to various cosmic factors. It then calculates a dynamic "Cosmic Priority Score" for each task, providing a clear, prioritized list to guide your actions in these uncertain times.

## Features

*   **Dynamic Prioritization**: Tasks are scored and sorted based on current cosmic factors.
*   **Configurable Cosmic Factors**: Define your own celestial influences (e.g., Lunar Alignment, Solar Flare Activity, Nebula Drift, Void Whisper Intensity) with their current values and impact multipliers.
*   **Task-Specific Modifiers**: Specify how much each individual task is affected by a given cosmic factor.
*   **Type-Safe**: Built with TypeScript for robust data handling and clarity.
*   **CLI Ready**: Easily integrate into nightly scripts or run manually.

## Installation

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/nightly-cosmic-chore-chart
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    # or
    yarn install
    ```

## Usage

The utility can be run directly via `ts-node` or after building with `tsc`.

### 1. Define Your Tasks and Cosmic Factors

Create a TypeScript file (e.g., `my-chores.ts`) or modify `src/index.ts` with your `Task` and `CosmicFactor` definitions.

**`src/types.ts`**:
```typescript
export interface CosmicFactor {
  name: string; // e.g., 'LunarAlignment'
  value: number; // Current intensity, e.g., 0.0 to 1.0
  impactMultiplier: number; // How much this factor influences priority (can be negative)
}

export interface Task {
  id: string;
  name: string;
  basePriority: number; // A baseline priority, higher is more urgent
  cosmicModifiers?: {
    [factorName: string]: number; // How much this specific task is affected by a cosmic factor (default: 1)
  };
  description?: string;
}

export interface PrioritizedTask extends Task {
  cosmicPriorityScore: number;
}
```

### 2. Run the Prioritizer

You can run the example directly:

```bash
npm start
# or
yarn start
```

To use your own custom tasks and factors:

```typescript
// my-chores.ts
import { prioritizeTasks, Task, CosmicFactor } from './src/index'; // Adjust path if needed

const myCosmicFactors: CosmicFactor[] = [
  { name: 'LunarAlignment', value: 0.8, impactMultiplier: 2 },
  { name: 'SolarFlareActivity', value: 0.2, impactMultiplier: 5 },
  // ... add more factors
];

const myTasks: Task[] = [
  {
    id: 'task-alpha',
    name: 'Fortify Shelter Perimeter',
    basePriority: 12,
    cosmicModifiers: { 'LunarAlignment': 1.8 }, // More urgent during lunar events
    description: 'Ensure defenses are robust.'
  },
  {
    id: 'task-beta',
    name: 'Scavenge for Rare Components',
    basePriority: 8,
    cosmicModifiers: { 'SolarFlareActivity': 0.5 }, // Less urgent during solar flares
    description: 'Seek out advanced tech scraps.'
  },
  // ... add more tasks
];

const prioritizedChart = prioritizeTasks(myTasks, myCosmicFactors);

console.log('\n--- My Prioritized Cosmic Chore Chart ---');
prioritizedChart.forEach((task, index) => {
  console.log(`${index + 1}. ${task.name}`);
  console.log(`   ID: ${task.id}`);
  console.log(`   Description: ${task.description}`);
  console.log(`   Base Priority: ${task.basePriority}`);
  console.log(`   Cosmic Priority Score: ${task.cosmicPriorityScore.toFixed(2)}`);
  console.log('---');
});
```

Then run it:
```bash
ts-node my-chores.ts
```

### Building for Production

For a compiled JavaScript version:

```bash
npm run build
```

This will compile the TypeScript files into the `dist/` directory. You can then run the compiled JavaScript:

```bash
node dist/index.js
```

## Development and Testing

### Running Tests

To ensure the cosmic calculations are precise and the prioritization is accurate, run the test suite:

```bash
npm test
# or
yarn test
```

### Project Structure

```
.
├── README.md
├── package.json
├── tsconfig.json
├── jest.config.js
├── src/
│   ├── index.ts        # Main logic for calculating and prioritizing tasks
│   └── types.ts        # TypeScript interfaces for tasks and cosmic factors
└── tests/
    └── index.test.ts   # Unit tests for the prioritization logic
```

## Contributing

Feel free to add more cosmic factors, refine the prioritization algorithm, or suggest new whimsical task types!
