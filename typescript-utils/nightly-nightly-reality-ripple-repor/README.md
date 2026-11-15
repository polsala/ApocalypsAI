# Nightly Reality Ripple Reporter

## Overview

The `nightly-reality-ripple-reporter` is a whimsical-yet-useful command-line interface (CLI) tool designed to help agents log and prioritize observed reality ripples or temporal anomalies. In the chaotic post-apocalyptic landscape, understanding and triaging these glitches is crucial. This tool provides a structured, type-safe way to report anomalies and get an immediate priority assessment.

## Features

*   **Type-Safe Reporting**: Define ripple characteristics with strict types.
*   **Automated Prioritization**: Get an instant priority (Low, Medium, High, Urgent) based on severity and type.
*   **CLI Interface**: Easy to use from the command line.

## Installation

1.  Ensure you have Node.js (v14 or higher) and npm/yarn installed.
2.  Navigate to the `typescript-utils/nightly-reality-ripple-reporter` directory.
3.  Install dependencies:
    ```bash
    npm install
    # or yarn install
    ```
4.  Build the TypeScript project:
    ```bash
    npm run build
    # or yarn build
    ```

## Usage

Run the CLI tool with the required parameters:

```bash
node dist/index.js report \
  --type <RippleType> \
  --severity <Severity> \
  --description "<A brief description of the ripple>" \
  --location "<Observed location>"
```

### Parameters:

*   `--type`: The type of ripple. Allowed values: `Temporal`, `Spatial`, `Causal`, `Echo`, `RealityDistortion`.
*   `--severity`: The perceived severity. Allowed values: `Minor`, `Moderate`, `Severe`, `Critical`.
*   `--description`: A short description of the ripple (e.g., "Sky turned green for 3 seconds").
*   `--location`: Where the ripple was observed (e.g., "Sector 7, Old Mall Ruins").

### Example:

```bash
node dist/index.js report \
  --type Temporal \
  --severity Severe \
  --description "Local time loop, repeating Tuesday for 10 minutes" \
  --location "Clock Tower Plaza"

# Expected Output:
# Reporting Reality Ripple:
#   ID: <generated-uuid>
#   Type: Temporal
#   Severity: Severe
#   Description: Local time loop, repeating Tuesday for 10 minutes
#   Location: Clock Tower Plaza
#   Observed At: <current-timestamp>
#   Assigned Priority: High
```

## Development

To run the TypeScript code directly (without building):

```bash
# Install ts-node for direct execution
npm install -g ts-node

ts-node src/index.ts report \
  --type Spatial \
  --severity Moderate \
  --description "Gravity fluctuations near the old power plant" \
  --location "Sector 3, Power Plant Perimeter"
```

## Tests

To run the automated tests:

```bash
npm test
# or yarn test
```
