# Nightly Temporal Harmonizer

The `nightly-temporal-harmonizer` is a whimsical-yet-useful utility designed to help individuals maintain mental equilibrium in the face of perceived minor temporal anomalies. When the fabric of time feels a little... off, this tool provides a specific, actionable "harmonization ritual" to help ground your perception and smooth out those temporal ripples.

## Features

*   **Anomaly Recognition**: Identifies common perceived temporal disturbances.
*   **Ritual Prescription**: Provides a unique, whimsical, and actionable ritual for each anomaly.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.

## Installation

To use this utility, you'll need Node.js and npm (or yarn) installed.

1.  Navigate to the `typescript-utils/nightly-temporal-harmonizer` directory.
2.  Install dependencies:
    ```bash
    npm install
    # or yarn install
    ```

## Usage

You can use this utility programmatically in your TypeScript/JavaScript projects.

### Get a ritual for a specific anomaly

```typescript
import { getHarmonizationRitual, TemporalAnomaly } from './src';

const anomaly: TemporalAnomaly = "déjà vu loop";
const ritual = getHarmonizationRitual(anomaly);

if (ritual) {
  console.log(`Anomaly: ${anomaly}`);
  console.log(`Title: ${ritual.title}`);
  console.log(`Description: ${ritual.description}`);
  console.log(`Action: ${ritual.action}`);
} else {
  console.log(`No ritual found for anomaly: ${anomaly}`);
}
```

### List all recognized temporal anomalies

```typescript
import { listTemporalAnomalies } from './src';

const anomalies = listTemporalAnomalies();
console.log("Recognized Temporal Anomalies:");
anomalies.forEach(anomaly => console.log(`- ${anomaly}`));
```

### Example Output

```
Anomaly: déjà vu loop
Title: The Familiar Passage
Description: To break the loop, re-engage with a known text.
Action: Re-read a familiar passage from a pre-collapse book, focusing on a single word you've never truly noticed before. This grounds your perception in linear progression.
```

## Development

### Running Tests

```bash
npm test
# or yarn test
```

### Building

```bash
npm run build
# or yarn build
```
