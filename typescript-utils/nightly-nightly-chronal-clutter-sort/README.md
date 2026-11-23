# Nightly Chronal Clutter Sorter

A whimsical TypeScript CLI tool designed to help the ApocalypsAI community make sense of the ever-increasing temporal anomalies and reality glitches. This utility allows users to define custom rules to categorize and prioritize these strange occurrences, bringing a semblance of order to the chaotic chronal landscape.

## Features

*   **Rule-based Categorization**: Define regex patterns to match anomaly descriptions and assign them to custom categories (e.g., "Temporal Tangle", "Reality Ripple", "Void Vortex").
*   **Priority Assignment**: Assign urgency levels (e.g., "Mild Concern", "Urgent Intervention", "Cosmic Catastrophe") to anomalies based on matching rules.
*   **CLI Interface**: Easily process anomaly logs from a JSON file and output a structured, prioritized report.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.

## Installation

1.  Navigate to the utility's directory:
    ```bash
    cd typescript-utils/nightly-chronal-clutter-sorter
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## Usage

The `chronal-sorter` command expects an input JSON file containing a list of anomalies and an optional configuration JSON file for rules.

```bash
./dist/cli.js --anomalies <path/to/anomalies.json> [--rules <path/to/rules.json>]
```

### Example `anomalies.json`

```json
[
  {
    "id": "ANOMALY-001",
    "description": "My coffee brewed itself yesterday, but it was tea.",
    "timestamp": "2024-07-20T08:30:00Z",
    "tags": ["domestic", "beverage", "temporal"]
  },
  {
    "id": "ANOMALY-002",
    "description": "A flock of flamingos briefly replaced the local pigeons.",
    "timestamp": "2024-07-19T14:15:00Z",
    "tags": ["wildlife", "visual", "reality-shift"]
  },
  {
    "id": "ANOMALY-003",
    "description": "The moon briefly turned into a giant disco ball.",
    "timestamp": "2024-07-18T22:00:00Z",
    "tags": ["celestial", "visual", "cosmic"]
  },
  {
    "id": "ANOMALY-004",
    "description": "My pet rock started quoting Shakespeare.",
    "timestamp": "2024-07-20T10:00:00Z",
    "tags": ["domestic", "sentient", "auditory"]
  }
]
```

### Example `rules.json`

```json
[
  {
    "pattern": "coffee|tea",
    "category": "Domestic Chronal Quirk",
    "priority": "Mild Concern"
  },
  {
    "pattern": "flamingos|pigeons",
    "category": "Fauna Flux",
    "priority": "Low Priority"
  },
  {
    "pattern": "moon.*disco ball",
    "category": "Cosmic Catastrophe",
    "priority": "Urgent Intervention"
  },
  {
    "pattern": "pet rock.*Shakespeare",
    "category": "Sentient Stone Syndrome",
    "priority": "Medium Priority"
  },
  {
    "pattern": "temporal",
    "category": "Temporal Tangle",
    "priority": "High Priority"
  }
]
```

### Output Example

```json
{
  "Cosmic Catastrophe": [
    {
      "id": "ANOMALY-003",
      "description": "The moon briefly turned into a giant disco ball.",
      "timestamp": "2024-07-18T22:00:00Z",
      "tags": ["celestial", "visual", "cosmic"],
      "priority": "Urgent Intervention"
    }
  ],
  "Temporal Tangle": [
    {
      "id": "ANOMALY-001",
      "description": "My coffee brewed itself yesterday, but it was tea.",
      "timestamp": "2024-07-20T08:30:00Z",
      "tags": ["domestic", "beverage", "temporal"],
      "priority": "High Priority"
    }
  ],
  "Sentient Stone Syndrome": [
    {
      "id": "ANOMALY-004",
      "description": "My pet rock started quoting Shakespeare.",
      "timestamp": "2024-07-20T10:00:00Z",
      "tags": ["domestic", "sentient", "auditory"],
      "priority": "Medium Priority"
    }
  ],
  "Fauna Flux": [
    {
      "id": "ANOMALY-002",
      "description": "A flock of flamingos briefly replaced the local pigeons.",
      "timestamp": "2024-07-19T14:15:00Z",
      "tags": ["wildlife", "visual", "reality-shift"],
      "priority": "Low Priority"
    }
  ]
}
```

## Development

To run tests:
```bash
npm test
```
