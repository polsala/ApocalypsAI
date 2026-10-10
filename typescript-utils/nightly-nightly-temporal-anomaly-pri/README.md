# Nightly Temporal Anomaly Prioritizer (Nightly-TAP)

A type-safe command-line utility for the ApocalypsAI community to categorize and prioritize detected temporal anomalies. In a world rife with temporal distortions, knowing which anomaly to tackle first is paramount. Nightly-TAP allows you to define custom rules to automatically assign priority scores and suggested actions, ensuring critical temporal tears don't go unnoticed.

## Features

*   **Rule-Based Prioritization**: Define JSON rules to match anomalies by type, severity, location, and data points.
*   **Dynamic Scoring**: Anomalies are assigned a priority score based on their inherent severity and matching rules.
*   **Action Suggestions**: Get immediate, context-aware action recommendations for each prioritized anomaly.
*   **Type-Safe**: Built with TypeScript for robust data handling and predictable outcomes.

## Installation

To use Nightly-TAP, you'll need Node.js (v14 or higher) and npm installed.

```bash
npm install -g nightly-temporal-anomaly-prioritizer
```

Alternatively, if running from the source directory:

```bash
npm install
npm run build
./bin/nightly-tap prioritize <anomalies_file.json> <rules_file.json>
```

## Usage

Run the `prioritize` command with your anomaly data and rule definitions:

```bash
nightly-tap prioritize <anomalies_file.json> <rules_file.json>
```

### Arguments

*   `<anomalies_file.json>`: Path to a JSON file containing an array of `Anomaly` objects.
*   `<rules_file.json>`: Path to a JSON file containing an array of `PrioritizationRule` objects.

### Example `anomalies.json`

```json
[
  {
    "id": "ANOMALY-001",
    "timestamp": "2023-10-27T10:00:00Z",
    "type": "temporal-drift",
    "severity": "moderate",
    "location": "Sector 7G",
    "description": "Minor time dilation detected.",
    "status": "detected",
    "detectedBy": "Sentry-Alpha",
    "dataPoints": 15
  },
  {
    "id": "ANOMALY-002",
    "timestamp": "2023-10-27T10:05:00Z",
    "type": "rift-signature",
    "severity": "critical",
    "location": "Void Edge",
    "description": "Large rift opening detected.",
    "status": "detected",
    "detectedBy": "Watcher-Omega",
    "dataPoints": 100
  }
]
```

### Example `rules.json`

```json
[
  {
    "name": "Critical Rift Alert",
    "condition": {
      "type": "rift-signature",
      "severity": "critical"
    },
    "action": "critical",
    "priorityBoost": 20
  },
  {
    "name": "Severe Temporal Drift in Hub",
    "condition": {
      "type": "temporal-drift",
      "severity": "severe",
      "locationContains": "Central Hub"
    },
    "action": "high",
    "priorityBoost": 10
  },
  {
    "name": "Minor Echo Chamber Ignore",
    "condition": {
      "type": "echo-chamber",
      "severity": "minor"
    },
    "action": "ignore"
  }
]
```

### Output

The tool will output a JSON array of `PrioritizedAnomaly` objects to `stdout`, sorted by `priorityScore` in descending order.

```json
[
  {
    "id": "ANOMALY-002",
    "timestamp": "2023-10-27T10:05:00Z",
    "type": "rift-signature",
    "severity": "critical",
    "location": "Void Edge",
    "description": "Large rift opening detected.",
    "status": "detected",
    "detectedBy": "Watcher-Omega",
    "dataPoints": 100,
    "priorityScore": 35,
    "assignedPriority": "critical",
    "matchedRules": [
      "Critical Rift Alert"
    ],
    "suggestedAction": "CRITICAL: Full team deployment to Void Edge for rift-signature. Containment protocols initiated."
  },
  ...
]
```

## Development

To build and test the utility:

```bash
npm install
npm run build
npm test
```
