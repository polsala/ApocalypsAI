# Nightly Chrono-Shard Sorter

## Overview

The `nightly-chrono-shard-sorter` is a whimsical-yet-useful TypeScript CLI utility designed to help the community manage and make sense of "chrono-shards" – temporal event logs that might be distorted or carry varying levels of urgency. In the chaotic temporal landscape, critical echoes can easily be lost. This tool allows you to load, sort, and filter these shards, ensuring that the most pressing temporal anomalies or resource alerts are brought to your attention.

## Features

*   **Load Shards**: Reads chrono-shard data from a JSON file.
*   **Sort Shards**: Sorts shards by `urgency`, `distortionLevel`, or `timestamp` in ascending or descending order.
*   **Filter Shards**: Filters shards by specific tags (e.g., 'anomaly', 'resource', 'system').
*   **Type-Safe**: Built with TypeScript for robust data handling and clear interfaces.

## Installation

To use this utility, you need Node.js (v14 or higher) and npm/yarn installed.

1.  Navigate to the `nightly-chrono-shard-sorter` directory.
2.  Install dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```
3.  Build the TypeScript project (optional, for running compiled JS):
    ```bash
    npm run build
    ```

## Usage

Run the utility using `ts-node` (for direct execution) or `node` (after building).

### Example `shards.json` format:

Create a JSON file (e.g., `my-shards.json`) with an array of chrono-shard objects:

```json
[
  {
    "id": "cs-001",
    "timestamp": "2023-10-26T14:30:00Z",
    "event": "Minor temporal ripple detected near Sector Gamma-7",
    "distortionLevel": "low",
    "urgency": "low",
    "tags": ["system", "temporal"]
  },
  {
    "id": "cs-002",
    "timestamp": "2023-10-26T15:05:10Z",
    "event": "Critical resource depletion warning: Antimatter reserves at 5%",
    "distortionLevel": "medium",
    "urgency": "high",
    "tags": ["resource", "alert"]
  },
  {
    "id": "cs-003",
    "timestamp": "2023-10-25T23:15:00Z",
    "event": "Anomaly signature matching 'Void Whisper' pattern detected",
    "distortionLevel": "critical",
    "urgency": "immediate",
    "tags": ["anomaly", "alert", "temporal"]
  },
  {
    "id": "cs-004",
    "timestamp": "2023-10-26T14:00:00Z",
    "event": "Routine system integrity check completed",
    "distortionLevel": "low",
    "urgency": "low",
    "tags": ["system"]
  }
]
```

### Command Line Options:

*   `-f, --file <path>`: **(Required)** Path to the JSON file containing chrono shards.
*   `-s, --sort-by <field>`: Field to sort shards by. Choices: `urgency`, `distortionLevel`, `timestamp`. Default: `timestamp`.
*   `-o, --order <direction>`: Sort order. Choices: `asc`, `desc`. Default: `asc`.
*   `-t, --filter-tag <tag>`: Filter shards by a specific tag.

### Examples:

1.  **Load and display all shards (sorted by timestamp ascending, default):**
    ```bash
    npm start -- --file ./my-shards.json
    ```
    or
    ```bash
    npx ts-node src/index.ts --file ./my-shards.json
    ```

2.  **Sort by urgency in descending order:**
    ```bash
    npm start -- --file ./my-shards.json --sort-by urgency --order desc
    ```

3.  **Filter by 'alert' tag and sort by distortion level ascending:**
    ```bash
    npm start -- --file ./my-shards.json --filter-tag alert --sort-by distortionLevel
    ```

4.  **Filter by 'temporal' tag and sort by timestamp descending:**
    ```bash
    npm start -- --file ./my-shards.json --filter-tag temporal --sort-by timestamp --order desc
    ```

## Development

### Running Tests

Tests are written with Jest and can be run using:

```bash
npm test
```

### Building the Project

To compile TypeScript to JavaScript:

```bash
npm run build
```

The compiled JavaScript files will be located in the `dist/` directory.
