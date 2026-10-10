# Nightly Temporal Echo Map

The Nightly Temporal Echo Map is a whimsical-yet-useful interactive React web application designed to visualize temporal anomalies and echoes across a grid. In a world where time itself can be... shifty, this tool helps the community identify hotspots of chronal instability, making it easier to navigate or avoid affected areas.

## Features

*   **Interactive Heatmap**: Displays a grid where each cell's "heat" (color intensity) represents the concentration or severity of temporal anomalies.
*   **Dynamic Data Simulation**: Includes a simple mechanism to simulate new anomaly detections, allowing users to observe how the map updates in real-time.
*   **Clear Visualization**: Provides an intuitive visual representation of temporal disturbances, aiding in strategic planning for survival and resource gathering.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd nightly-temporal-echo-map
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```
3.  **Start the development server**:
    ```bash
    npm start
    # or yarn start
    ```
    This will open the application in your default web browser, usually at `http://localhost:3000`.

## How to Use

Once the application is running:

*   Observe the grid: Each square represents a segment of space-time.
*   Color intensity indicates anomaly severity: Darker/redder cells signify higher anomaly activity.
*   Click the "Simulate New Anomaly" button to add a random new anomaly to the map and see the visualization update.

## Project Structure

```
.
├── README.md
├── package.json
├── src/
│   ├── index.html          # Main HTML file
│   ├── index.jsx           # React app entry point
│   ├── App.jsx             # Main application component
│   ├── components/
│   │   ├── AnomalyMap.jsx  # Heatmap visualization component
│   │   └── AnomalyMap.css  # Styling for the heatmap
│   └── data/
│       └── mockAnomalies.js # Mock data for initial display and testing
└── tests/
    └── AnomalyMap.test.jsx # Jest tests for the AnomalyMap component
```
