# Nightly Resource Manifest Auditor (nightly-resource-manifest-aud)

## Overview

In the chaotic aftermath, maintaining a balanced inventory of vital resources is paramount. The `nightly-resource-manifest-aud` is a whimsical-yet-critical TypeScript utility designed to audit your current resource holdings against a desired manifest. It highlights critical shortages, unexpected surpluses, and confirms optimal balances, ensuring your survival cache is always prepared for the next temporal anomaly or wasteland expedition.

## Features

*   **Type-Safe Auditing**: Leverages TypeScript for robust, error-checked manifest comparisons.
*   **Shortage Detection**: Identifies resources where your current supply falls below the desired threshold.
*   **Surplus Identification**: Flags resources present in your current stash but not explicitly listed in your desired manifest, or in excess of what's needed.
*   **Whimsical Resource Definitions**: Comes with a set of predefined, apocalypse-appropriate resource types.
*   **CLI Interface**: Easy to use from your terminal with JSON input/output.

## Installation

1.  Navigate to the utility's directory:
    ```bash
    cd nightly-resource-manifest-aud
    ```
2.  Install dependencies:
    ```bash
    npm install
    # or yarn install
    ```

## Usage

The utility expects two JSON files as input: one for your `desired` resource manifest and one for your `current` resource manifest.

### Manifest Format

Both `desired.json` and `current.json` should be simple key-value pairs where the key is the resource name (string) and the value is the quantity (number).

Example `desired.json`:
```json
{
  "Nutrient Paste": 100,
  "Hydro-Purification Tablets": 50,
  "Temporal Stabilizers": 5,
  "Glimmering Dust": 20
}
```

Example `current.json`:
```json
{
  "Nutrient Paste": 80,
  "Hydro-Purification Tablets": 60,
  "Temporal Stabilizers": 5,
  "Quantum Entanglement String": 2
}
```

### Running the Auditor

```bash
# Using ts-node for direct execution (requires ts-node installed globally or locally)
# npm install -g ts-node

ts-node src/index.ts <path/to/desired.json> <path/to/current.json>

# Example:
ts-node src/index.ts desired.json current.json
```

This will output a JSON array representing the audit report to `stdout`.

### Example Output

```json
[
  {
    "resourceName": "Nutrient Paste",
    "status": "shortage",
    "needed": 100,
    "current": 80,
    "difference": -20,
    "message": "Critical Shortage! You need 20 more Nutrient Paste (cans)."
  },
  {
    "resourceName": "Hydro-Purification Tablets",
    "status": "surplus",
    "needed": 50,
    "current": 60,
    "difference": 10,
    "message": "Unexpected Surplus! You have 10 more Hydro-Purification Tablets (tablets) than desired."
  },
  {
    "resourceName": "Temporal Stabilizers",
    "status": "ok",
    "needed": 5,
    "current": 5,
    "difference": 0,
    "message": "Optimal Balance Achieved for Temporal Stabilizers."
  },
  {
    "resourceName": "Glimmering Dust",
    "status": "shortage",
    "needed": 20,
    "current": 0,
    "difference": -20,
    "message": "Critical Shortage! You need 20 more Glimmering Dust (grams)."
  },
  {
    "resourceName": "Quantum Entanglement String",
    "status": "surplus",
    "needed": 0,
    "current": 2,
    "difference": 2,
    "message": "Unexpected Surplus! Quantum Entanglement String is not in your desired manifest, but you have 2 (meters)."
  }
]
```

## Development

### Running Tests

```bash
npm test
# or yarn test
```
