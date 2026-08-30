# Nightly Temporal Echo Visualizer

## Overview

The `nightly-temporal-echo-visualizer` is a whimsical-yet-useful React web application designed to help the community monitor and understand simulated temporal anomalies. It provides an interactive timeline visualization of 'temporal echoes' – events where the fabric of time might be rippling, distorting, or even tearing. While the data is currently simulated, this tool lays the groundwork for future integration with real-time temporal anomaly detection systems.

## Features

*   **Interactive Timeline**: Visualize temporal echoes chronologically.
*   **Echo Details**: Click on any echo marker to view its type, magnitude, location, and a brief description.
*   **Simulated Data**: Comes pre-loaded with mock temporal echo data for immediate use and demonstration.

## Installation & Setup

To run this utility, you need Node.js and npm (or yarn) installed on your system.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-temporal-echo-visualizer
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

## Usage

Once the application is running:

1.  Observe the timeline displaying various temporal echo markers.
2.  Click on any echo marker (represented by a colored dot) to reveal its detailed information in the panel below the timeline.
3.  The details panel will update to show the `Type`, `Magnitude`, `Location`, and `Description` of the selected echo.

## Mock Data

The application uses `src/data/mockEchoes.js` for its data source. This allows for deterministic testing and offline functionality. You can modify this file to experiment with different temporal echo scenarios.

## Development

*   **`src/App.js`**: The main application component, responsible for fetching (mock) data and orchestrating the layout.
*   **`src/components/EchoTimeline.js`**: Renders the interactive timeline and individual echo markers.
*   **`src/data/mockEchoes.js`**: Contains the static, simulated temporal echo data.
*   **`tests/App.test.js`**: Contains unit tests for the main application component.
