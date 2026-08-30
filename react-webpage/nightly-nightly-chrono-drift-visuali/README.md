# Nightly Chrono-Drift Visualizer

The Nightly Chrono-Drift Visualizer is a whimsical-yet-crucial React web application designed to help the community track and understand temporal anomalies and drifts across the post-apocalyptic landscape. By presenting these distortions on an interactive, stylized map, survivors can gain insights into areas of temporal instability, potential resource fluctuations, or even pockets of accelerated/decelerated time.

## Features

*   **Interactive Map**: A visual representation of the wasteland with key areas.
*   **Anomaly Visualization**: Temporal drifts are depicted as pulsating, color-coded markers.
*   **Detailed Insights**: Click on an anomaly to view its "Temporal Resonance Frequency," "Drift Magnitude," and "Estimated Impact Radius."
*   **Simulated Data**: Uses mock data to demonstrate functionality, easily extendable for real-time feeds.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-chrono-drift-visualizer
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Start the development server**:
    ```bash
    npm start
    ```
    This will typically open the application in your browser at `http://localhost:3000`.

## Project Structure

```
.
├── README.md
├── package.json
├── public/
│   └── index.html      # Main HTML file
├── src/
│   ├── App.css         # Basic styling
│   ├── App.js          # Main React component
│   ├── AnomalyMap.js   # Component for rendering the map and anomalies
│   ├── AnomalyDetails.js # Component for displaying anomaly details
│   ├── data/
│   │   └── mockAnomalies.js # Mock data for anomalies
│   └── index.js        # React app entry point
└── tests/
    └── App.test.js     # Tests for the main App component
```

## Technologies Used

*   React
*   Create React App (for basic setup)
*   CSS Modules (or simple CSS)

## Contributing

Feel free to expand the anomaly types, add more sophisticated visualization, or integrate with actual temporal data feeds (if you can find any stable ones).
