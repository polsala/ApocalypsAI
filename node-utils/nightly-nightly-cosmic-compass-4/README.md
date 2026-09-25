# Nightly Cosmic Compass

A whimsical Node.js utility that generates celestial navigation coordinates for fictional star systems. Perfect for adding a touch of cosmic flair to your tabletop RPGs, creative writing projects, or just for fun.

## Features

*   Generates random star system names.
*   Assigns unique celestial coordinates (e.g., Galactic Sector, Quadrant, Star Cluster, Star Designation).
*   Provides a brief, imaginative description for each star system.

## Installation

```bash
npm install @polsala/nightly-cosmic-compass
```

## Usage

### Command Line Interface (CLI)

Run the utility directly from your terminal:

```bash
npx @polsala/nightly-cosmic-compass
```

This will output a single, randomly generated star system with its coordinates and description.

### Programmatic Usage (Node.js)

```javascript
const cosmicCompass = require('@polsala/nightly-cosmic-compass');

async function generateSystem() {
  const system = await cosmicCompass.generateStarSystem();
  console.log(`Star System: ${system.name}`);
  console.log(`Coordinates: ${system.coordinates.sector} ${system.coordinates.quadrant} ${system.coordinates.cluster} ${system.coordinates.designation}`);
  console.log(`Description: ${system.description}`);
}

generateSystem();
```

## Development

To run the tests locally:

```bash
npm install
npm test
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
