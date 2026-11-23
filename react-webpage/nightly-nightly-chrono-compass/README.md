# Nightly Chrono-Compass

An interactive web dashboard to visualize and track detected temporal anomalies and their stabilization status within the ApocalypsAI network. This utility provides a clear, real-time (simulated) overview of temporal distortions, helping agents prioritize stabilization efforts.

## Features

*   **Anomaly List:** Displays a list of detected temporal anomalies with unique IDs, types (e.g., "Minor Drift", "Echo Cascade", "Rift Tear"), severity levels, and current stabilization status.
*   **Status Indicators:** Visual cues for anomaly status (e.g., "Unstable", "Stabilizing", "Stabilized").
*   **Simulated Stabilization:** A button to simulate the stabilization process for all displayed anomalies.
*   **Whimsical Interface:** A user-friendly, thematic interface designed for easy monitoring.

## Installation and Usage

This utility requires Node.js and npm.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-chrono-compass
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Start the development server:**
    ```bash
    npm start
    ```
    This will open the Chrono-Compass in your browser, usually at `http://localhost:3000`.

## Project Structure

```
.
├── README.md
├── package.json
├── src/
│   ├── App.css
│   ├── App.js
│   ├── index.css
│   ├── index.html
│   └── index.js
└── tests/
    └── App.test.js
```

## Automated Tests

To run the automated tests:

```bash
npm test
```

The tests use Jest and React Testing Library to ensure the component renders correctly and displays the mock anomaly data as expected.

## Mock Rationale

*   **Anomaly Data:** The `fetchAnomalies` function in `src/App.js` is mocked to return a static array of temporal anomalies. In a real-world scenario, this would fetch data from an ApocalypsAI backend API (e.g., `nightly-temporal-anomaly-tracker` or `nightly-temporal-drift-detector`). This mocking ensures the utility is self-contained and tests are deterministic and offline.
*   **Stabilization Process:** The "Initiate Global Stabilization" button's functionality is simulated by updating the local state of anomalies. A real implementation would trigger an API call to a stabilization service. This keeps the utility focused on the UI aspect.
