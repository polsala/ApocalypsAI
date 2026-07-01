# Nightly Temporal Anomaly Manifest Generator

## Summary
`nightly-anomaly-manifest-gen` is a whimsical-yet-useful command-line utility designed to help the community categorize and prioritize observed anomalous phenomena. It takes raw descriptions of temporal, spatial, or reality-bending events and generates a structured, type-safe JSON manifest, automatically classifying each anomaly by category and severity based on keywords.

This tool is built with TypeScript to ensure data consistency and provide a robust foundation for tracking the strange occurrences in our ever-shifting reality.

## Installation
To use this utility, you need Node.js and npm (or yarn) installed.

1.  Navigate to the utility's directory:
    ```bash
    cd typescript-utils/nightly-anomaly-manifest-gen
    ```
2.  Install dependencies and build the project:
    ```bash
    npm install
    npm run build
    ```
3.  (Optional) Link the utility globally for easy access:
    ```bash
    npm link
    # Now you can run 'anomaly-manifest-gen' from any directory
    ```

## Usage
The utility reads a JSON array of anomaly input objects from standard input (`stdin`) and outputs a structured JSON array of anomaly manifest entries to standard output (`stdout`).

### Input Format (`AnomalyInput[]`)
Each input object should conform to the following structure:

```typescript
interface AnomalyInput {
  description: string; // A detailed description of the anomaly
  location?: string;   // Optional: Where the anomaly was observed
  observedBy?: string; // Optional: Who observed the anomaly
}
```

**Example Input (`input.json`):**
```json
[
  {
    "description": "A subtle time distortion observed near the old clock tower, causing clocks to run backwards for brief moments.",
    "location": "Clock Tower Plaza",
    "observedBy": "Chronos Watcher Unit 7"
  },
  {
    "description": "Reality flickers in Sector 7, causing objects to briefly disappear and reappear. Moderate disruption to local commerce.",
    "location": "Sector 7 Market",
    "observedBy": "Scavenger Guild Patrol"
  },
  {
    "description": "Critical energy surge detected at Power Station Alpha, leading to a complete grid collapse and localized EMP effects.",
    "location": "Power Station Alpha"
  }
]
```

### Output Format (`AnomalyManifestEntry[]`)
Each output object will have a unique ID, timestamp, and auto-classified category and severity:

```typescript
interface AnomalyManifestEntry {
  id: string;             // Unique identifier for the anomaly
  timestamp: string;      // ISO 8601 timestamp of manifest generation
  description: string;
  location?: string;
  observedBy?: string;
  category: "Temporal Distortion" | "Reality Glitch" | "Spatial Displacement" | "Energy Fluctuation" | "Biological Mutation" | "Unknown";
  severity: "Minor" | "Moderate" | "Severe" | "Critical" | "Unknown";
  notes?: string;         // Auto-generated classification notes
}
```

### Running the Utility

Pipe your JSON input file to the utility:

```bash
cat input.json | anomaly-manifest-gen > manifest.json
```

Or, if you linked it globally:

```bash
anomaly-manifest-gen < input.json > manifest.json
```

### Classification Logic
The utility uses keyword matching within the `description` field to determine `category` and `severity`.

**Categories:**
*   `Temporal Distortion`: "time", "temporal", "loop", "echo", "chronal"
*   `Reality Glitch`: "reality", "glitch", "flicker", "impossible", "paradox"
*   `Spatial Displacement`: "space", "spatial", "teleport", "displace", "rift"
*   `Energy Fluctuation`: "energy", "power", "surge", "radiation", "flux"
*   `Biological Mutation`: "creature", "mutation", "flora", "fauna", "organic"
*   `Unknown`: If no specific keywords are found.

**Severities:**
*   `Critical`: "critical", "catastrophic", "imminent", "apocalyptic"
*   `Severe`: "severe", "dangerous", "major", "hazardous"
*   `Moderate`: "moderate", "noticeable", "disruptive", "significant"
*   `Minor`: "minor", "slight", "subtle", "insignificant"
*   `Unknown`: If no specific keywords are found.

If multiple keywords for different categories/severities are present, the first match in the internal logic determines the classification. The `notes` field will indicate the auto-classification and suggest manual review.

## Development

### Running Tests
```bash
npm test
```

### Building
```bash
npm run build
```

This will compile the TypeScript code from `src/` into JavaScript in the `dist/` directory.
