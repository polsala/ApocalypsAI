# Nightly Chrono-Weave Visualizer

## Summary

Welcome to the Nightly Chrono-Weave Visualizer! This whimsical React web application offers a playful yet insightful way to observe simulated temporal data streams. Imagine data flowing through the fabric of time as 'chrono-threads'. This tool visualizes these threads, and when an 'anomaly' occurs, it manifests as a delightful, temporary distortion in the weave – a wiggle, a color shift, or a shimmering ripple.

It's designed to be a fun, interactive dashboard for understanding patterns and detecting unusual events in a continuous data flow, presented with a touch of ApocalypsAI charm.

## How to Run

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-chrono-weave-visualizer
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

## How to Use

Once the application is running, you'll see a canvas with several 'chrono-threads' flowing across it. A control panel at the top allows you to interact with the simulation:

*   **Start/Stop Button:** Toggles the data stream visualization on or off.
*   **Speed Slider:** Adjusts how fast the chrono-threads move and update. Higher speed means faster data flow.
*   **Anomaly Frequency Slider:** Controls how often 'anomalies' occur. A higher frequency means more frequent visual distortions in the threads.

Observe the threads for changes in color, position, or shape, which indicate a detected anomaly. Enjoy the dance of data!

## Project Structure

*   `public/`: Standard Create React App public assets.
*   `src/`: React application source code.
    *   `App.js`: The main application component, handling global state and controls.
    *   `ChronoWeave.js`: The core visualization component, managing threads and animation.
    *   `ChronoThread.js`: Renders a single 'chrono-thread' with its current state and anomaly effects.
    *   `AnomalyDetector.js`: A utility for determining if and how long an anomaly should occur.
    *   `index.js`: Entry point for the React application.
    *   `index.css`: Basic styling for the application.
*   `package.json`: Project dependencies and scripts.
*   `tests/`: Unit tests for React components and utility functions.
