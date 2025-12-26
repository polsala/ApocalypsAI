# Nightly Chronal Fragment Harmonizer

A TypeScript CLI tool designed to assist in the daunting task of integrating disparate data fragments salvaged from various temporal anomalies and post-collapse sources. It sorts, categorizes, and provides recommendations based on each fragment's "temporal distortion" level and timestamp, ensuring that the most stable and relevant data is prioritized for integration.

## Features

-   **Fragment Validation**: Ensures input data adheres to a strict `DataFragment` structure.
-   **Temporal Sorting**: Fragments are sorted first by their `temporalDistortion` (least distorted first) and then by `timestamp` (oldest first).
-   **Categorization**: Fragments are classified into 'Stable', 'Unstable', and 'Highly Distorted' based on their distortion score.
-   **Harmonization Report**: Generates a comprehensive report summarizing the findings and offering actionable recommendations for data integration.
-   **Type-Safe**: Built with TypeScript for robust data handling and fewer runtime surprises.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v18 or higher) and npm/yarn installed.
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-chronal-fragment-harmonizer
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```
4.  **Build the project**:
    ```bash
    npm run build
    ```
    This will compile the TypeScript code into JavaScript in the `dist/` directory.

## Usage

The `harmonize-fragments` command expects a path to a JSON file containing an array of `DataFragment` objects.

### Input Data Format (`fragments.json`)

Your input JSON file should be an array of objects, each conforming to the `DataFragment` interface:

```typescript
interface DataFragment {
  id: string;
  content: string;
  timestamp: string; // ISO 8601 string (e.g., "2042-03-15T10:30:00Z")
  temporalDistortion: number; // A number between 0 and 100 (lower is better)
  origin: string; // E.g., "Pre-Collapse Archive", "Wasteland Scavenge", "Void Echo"
}
```

**Example `fragments.json`:**
```json
[
  {
    "id": "frag-001",
    "content": "Old world news snippet about AI ethics.",
    "timestamp": "2042-03-15T10:30:00Z",
    "temporalDistortion": 15,
    "origin": "Pre-Collapse Archive"
  },
  {
    "id": "frag-002",
    "content": "Scavenged log entry: 'Power fluctuations detected near Sector 7.'",
    "timestamp": "2077-11-20T08:00:00Z",
    "temporalDistortion": 80,
    "origin": "Wasteland Scavenge"
  },
  {
    "id": "frag-003",
    "content": "A faint echo of a forgotten lullaby.",
    "timestamp": "2030-01-01T00:00:00Z",
    "temporalDistortion": 5,
    "origin": "Void Echo"
  },
  {
    "id": "frag-004",
    "content": "Partial schematic for a temporal capacitor.",
    "timestamp": "2050-07-22T14:15:00Z",
    "temporalDistortion": 45,
    "origin": "Pre-Collapse Archive"
  }
]
```

### Running the Harmonizer

```bash
./dist/cli.js ./fragments.json
# Or, if you added it to your PATH or linked it:
# harmonize-fragments ./fragments.json
```

**Example Output:**
```
Chronal Fragment Harmonization Report

Total Fragments Processed: 4
Stable Fragments (Distortion < 20): 2
Unstable Fragments (Distortion 20-60): 1
Highly Distorted Fragments (Distortion > 60): 1

--- Stable Fragments ---
[frag-003] (Void Echo) 2030-01-01T00:00:00Z - Distortion: 5
  Content: A faint echo of a forgotten lullaby.
[frag-001] (Pre-Collapse Archive) 2042-03-15T10:30:00Z - Distortion: 15
  Content: Old world news snippet about AI ethics.

--- Unstable Fragments ---
[frag-004] (Pre-Collapse Archive) 2050-07-22T14:15:00Z - Distortion: 45
  Content: Partial schematic for a temporal capacitor.

--- Highly Distorted Fragments ---
[frag-002] (Wasteland Scavenge) 2077-11-20T08:00:00Z - Distortion: 80
  Content: Scavenged log entry: 'Power fluctuations detected near Sector 7.'

--- Harmonization Recommendations ---
- Prioritize integration of 'Stable Fragments' first, as they exhibit minimal temporal distortion.
- 'Unstable Fragments' may require pre-processing or additional temporal stabilization before full integration.
- 'Highly Distorted Fragments' should be quarantined and analyzed for potential temporal anomalies before any integration attempts. Proceed with extreme caution.
- Consider cross-referencing fragments from 'Void Echo' origins for unique insights into pre-collapse timelines, but verify their stability.
```

## Development

### Running Tests

```bash
npm test
# or yarn test
```

### Linting and Formatting

```bash
npm run lint
npm run format
```

## Contributing

Contributions are welcome! Please ensure your changes adhere to the existing code style, include appropriate tests, and update the documentation.
