# Nightly Temporal Anomaly Visualizer

## Summary

The `nightly-temporal-anomaly-viz` is an interactive React web dashboard designed to provide a whimsical yet useful visualization of detected temporal anomalies. It allows the community to observe, track, and (simulated) stabilize temporal distortions, offering a clear overview of the spacetime continuum's current state.

## Features

*   **Anomaly Listing**: Displays a list of detected temporal anomalies with their unique IDs, types, severity levels, and timestamps.
*   **Severity Indicators**: Visual cues (e.g., color-coding, glitch effects for critical anomalies) to quickly identify the most critical areas.
*   **Simulated Stabilization**: A button to 'stabilize' an anomaly, demonstrating potential interaction with temporal distortion fields.
*   **Mock Data Integration**: Uses local mock data for demonstration, making it fully self-contained and runnable offline.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-temporal-anomaly-viz
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Start the development server**:
    ```bash
    npm start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

## How to Test

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-temporal-anomaly-viz
    ```
2.  **Run tests**:
    ```bash
    npm test
    ```

## Project Structure

```
react-webpage/nightly-temporal-anomaly-viz/
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.css
│   ├── App.js
│   ├── index.js
│   ├── components/
│   │   ├── AnomalyCard.js
│   │   └── AnomalyDashboard.js
│   └── data/
│       └── mockAnomalies.js
└── tests/
    ├── App.test.js
    └── AnomalyDashboard.test.js
```
