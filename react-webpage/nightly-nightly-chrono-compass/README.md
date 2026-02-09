# Nightly Chrono-Compass: Temporal Anomaly Visualizer

## Summary

The Nightly Chrono-Compass is a whimsical-yet-useful React web application designed to provide the community with an interactive visualization of simulated temporal anomalies and drifts. It helps users quickly grasp the current state of temporal stability by displaying detected events on a timeline-like interface, allowing for easy monitoring of the spacetime continuum.

## Features

*   **Anomaly Listing**: Displays a list of simulated temporal anomalies with details like timestamp, type, severity, and description.
*   **Whimsical UI**: A simple, intuitive interface with a 'chrono-compass' aesthetic.
*   **Self-Contained**: Runs as a standalone React application.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-chrono-compass
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

4.  **Build for production (optional)**:
    ```bash
    npm run build
    ```
    This creates a `build` directory with optimized static files for deployment.

## How to Use

Once the application is running, you will see a list of simulated temporal anomalies. Each entry provides key information about the anomaly. The interface is designed for quick overview and monitoring.

## Project Structure

```
nightly-chrono-compass/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   └── ChronoCompass.js  # Main visualization component
│   ├── data/
│   │   └── mockAnomalies.js  # Simulated anomaly data
│   ├── App.js                # Root application component
│   └── index.js              # React entry point
├── tests/
│   └── ChronoCompass.test.js # Jest tests for the ChronoCompass component
├── package.json
└── README.md
```

## Mock Data

The application uses `src/data/mockAnomalies.js` to simulate temporal anomaly data. In a real-world scenario, this data would be fetched from a backend service or another ApocalypsAI agent's output. For this standalone utility, mock data ensures immediate functionality and testability.
