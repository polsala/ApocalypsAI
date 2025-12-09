# Apoc Resource Scanner

A whimsical yet practical TypeScript utility for simulating the discovery and categorization of scarce resources in a post-apocalyptic world.

## Features

*   **Resource Discovery**: Simulates finding various resource types.
*   **Categorization**: Organizes found resources into logical groups (e.g., 'Edibles', 'Materials', 'Tech').
*   **Rarity Simulation**: Assigns a rarity level to each discovered resource.
*   **Type Safety**: Leverages TypeScript for robust and predictable code.

## Installation

1.  **Prerequisites**: Node.js and npm (or yarn) installed.
2.  **Clone the repository** (if not already present).
3.  **Navigate to the utility directory**: `cd utils/nightly-apoc-resource-scanner`
4.  **Install dependencies**: `npm install` or `yarn install`

## Usage

Run the scanner from your terminal:

```bash
npx ts-node src/main.ts
```

### Options

*   `--count <number>`: Specify the number of resources to scan for (default: 10).
*   `--seed <number>`: Provide a seed for deterministic random generation (useful for testing).

**Example**: Scan for 25 resources with a specific seed:

```bash
npx ts-node src/main.ts --count 25 --seed 12345
```

## Development

To build and run the utility locally:

1.  **Install dependencies**: `npm install` or `yarn install`
2.  **Build the project**: `npm run build` or `yarn build`
3.  **Run the compiled JavaScript**: `node dist/main.js`

## Testing

Run the automated tests:

```bash
npm test` or `yarn test`
```

## Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.
