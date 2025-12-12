# Nightly Temporal Echo Map

A whimsical-yet-useful interactive web interface for visualizing and managing chronal disturbances across the ApocalypsAI wasteland. Keep an eye on temporal ripples, echo cascades, and void whispers, and take action to stabilize them!

## Features

*   **Interactive Map:** Visualize temporal anomalies at their detected locations.
*   **Anomaly Details:** Click or hover over markers to view detailed information about each disturbance.
*   **Stabilization Protocol:** Initiate a simulated stabilization process for active anomalies.
*   **Anomaly Log:** A real-time list of all detected temporal events.
*   **Retro-Futuristic UI:** A console-like interface fitting the ApocalypsAI aesthetic.

## How to Run

This utility is a standard React application.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-temporal-echo-map
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Start the development server:**
    ```bash
    npm start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

4.  **Build for production (optional):**
    ```bash
    npm run build
    ```
    This will create a `build` directory with the optimized production build.

## How to Test

To run the automated tests for this utility:

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-temporal-echo-map
    ```

2.  **Run the tests:**
    ```bash
    npm test -- --watchAll=false
    ```
    The `--watchAll=false` flag ensures tests run once and exit, suitable for CI/CD environments.

## Mock Rationale for Tests

*   **`AnomalyData.js` Mocking:** In `tests/App.test.js`, the `AnomalyData` module is mocked. This is crucial for ensuring deterministic and isolated tests. Instead of relying on actual data fetching or mutable global state, the mock provides predefined anomaly data. This allows tests to control the initial state and simulate the effect of `stabilizeAnomaly` without side effects, making tests reliable and fast.
*   **`window.alert` Mocking:** In `tests/App.test.js`, `window.alert` is mocked to prevent the browser's alert dialog from appearing during tests, which would halt execution and require manual intervention. This ensures the test runs non-interactively.
*   **`AnomalyMap.js` Isolation:** In `tests/AnomalyMap.test.js`, the `AnomalyMap` component is tested in isolation. It receives `anomalies` and `onStabilize` as props. The `onStabilize` prop is mocked to verify that the component correctly triggers the stabilization callback when a user interacts with the UI, without needing to know how `onStabilize` is implemented in the parent component.
