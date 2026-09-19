# Nightly Temporal Echo-Location Visualizer

## Overview

The `nightly-temporal-echo-viz` is a whimsical-yet-useful React web application designed to help the community visualize and track temporal echoes and anomalies across a grid-based map. In a world where temporal distortions are a daily occurrence, understanding their location and intensity can be crucial for safe navigation, resource gathering, and avoiding hazardous zones.

Simply click on any cell in the grid to 'ping' that location for temporal echoes. The map will then display the detected anomaly's strength and type, providing a visual guide to the temporal landscape.

## Features

*   **Interactive Grid Map**: A visual representation of a localized area.
*   **Temporal Ping**: Click any cell to simulate a temporal echo detection.
*   **Anomaly Visualization**: Echoes are displayed with varying colors and sizes based on their strength and type.
*   **Deterministic Echoes**: For consistency and testing, certain coordinates yield predictable echo types.

## Installation

To get this utility up and running, ensure you have Node.js and npm installed.

1.  Navigate to the `nightly-temporal-echo-viz` directory:
    ```bash
    cd react-webpage/nightly-temporal-echo-viz
    ```
2.  Install the necessary dependencies:
    ```bash
    npm install
    ```

## Usage

To start the development server and view the application in your browser:

```bash
npm start
```

This will typically open the application at `http://localhost:3000`. Once loaded, simply click on any square in the grid to perform a temporal ping and reveal any echoes present at that location.

## Development

### Running Tests

To run the automated tests for the application:

```bash
npm test
```

This will execute the Jest tests, ensuring the components render correctly and the echo detection logic behaves as expected.
