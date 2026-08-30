# Nightly Temporal Drift Dashboard

## Overview

The `nightly-temporal-drift-dash` is a whimsical-yet-useful React-based web application designed to provide a visual overview of temporal drift anomalies detected within the ApocalypsAI network. It allows community members to quickly identify periods of significant temporal instability, track the severity of drifts, and monitor the overall 'temporal health' of our reality.

## Features

*   **Interactive Timeline**: Visualize temporal drift events over a simulated timeline.
*   **Severity Indicators**: Clearly see the intensity of each detected drift.
*   **Anomaly Details**: Click on a drift event to view more details (simulated).
*   **Responsive Design**: Works on various screen sizes.

## Installation

To set up and run the dashboard locally, ensure you have Node.js (v14 or higher) and npm (or yarn) installed.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-temporal-drift-dash
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```

## Usage

1.  **Start the development server**:
    ```bash
    npm start
    # or yarn start
    ```
    This will open the dashboard in your default web browser, usually at `http://localhost:3000`.

2.  **Interact with the dashboard**: The dashboard will display a simulated timeline of temporal drift events. Each event will have a visual indicator of its severity.

## Development

To build the production-ready application:

```bash
npm run build
# or yarn build
```

This will create a `build` directory with the static assets.

## Testing

To run the automated tests:

```bash
npm test
# or yarn test
```

### Mock Rationale:

Tests for this React application utilize Jest and React Testing Library. Data fetching is mocked to ensure tests are deterministic and run offline. The `fetchDriftData` function, which simulates an API call, is replaced with a hardcoded dataset within the test environment. This guarantees consistent test results regardless of external factors or network availability.
