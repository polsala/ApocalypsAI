# Nightly Chrono-Compass Dashboard

## Overview

The `nightly-chrono-compass-dash` is a whimsical-yet-useful interactive React web application that provides a consolidated view of various ApocalypsAI community metrics. It features a "Chrono-Compass" that visually indicates the overall "Apocalypse Status" based on simulated data for temporal stability, resource abundance, community morale, and weather anomalies. This dashboard serves as a central hub for quick insights into the state of our post-apocalyptic world.

## Features

*   **Chrono-Compass**: A dynamic compass needle that points to the current "Apocalypse Status" (e.g., "Stable Temporal Flow", "Minor Reality Glitch", "Resource Scarcity Alert", "Imminent Chrono-Collapse").
*   **Metric Readouts**: Displays key metrics such as Temporal Stability Index, Resource Abundance Level, Community Morale Pulse, and Simulated Weather Anomaly.
*   **Interactive Updates**: The dashboard data and compass status update periodically to reflect changing conditions (simulated).

## How to Run

To run this utility, you need Node.js and npm (or yarn) installed.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-chrono-compass-dash
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
    This will open the application in your browser, usually at `http://localhost:3000`.

4.  **Build for production (optional)**:
    ```bash
    npm run build
    # or yarn build
    ```
    This creates a `build` directory with the production-ready static files.

## How it Works

The dashboard uses React to render an interactive user interface. It simulates fetching data from various ApocalypsAI systems (like temporal anomaly detectors, resource trackers, etc.) using `setTimeout` to periodically update the displayed metrics. The Chrono-Compass component then interprets these metrics to determine and display the overall "Apocalypse Status."

## Project Structure

```
.
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.js
│   ├── ChronoCompass.js
│   ├── index.js
│   └── styles.css
└── tests/
    ├── App.test.js
    └── ChronoCompass.test.js
```
