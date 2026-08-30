# Nightly Temporal Echo Visualizer

An interactive React web interface to visualize and filter simulated temporal echoes and anomalies.

## Overview

The `nightly-temporal-echo-viz` provides a whimsical yet useful dashboard for observing "temporal echoes" – simulated distortions and anomalies in the fabric of time. It allows users to view a stream of these echoes, filter them by type and intensity, and gain a better understanding of the temporal landscape.

This utility is designed to complement other "temporal" utilities within the ApocalypsAI ecosystem, offering a visual representation of their detected phenomena.

## Features

*   **Echo Stream**: Displays a list of simulated temporal echoes with their ID, type, intensity, timestamp, and description.
*   **Filtering**: Filter echoes by their type (e.g., "Temporal Ripple", "Chronal Feedback") and by a minimum intensity level.
*   **Interactive UI**: A responsive and easy-to-use web interface built with React.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-temporal-echo-viz
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
    This creates a `build` directory with optimized static files.

## How it Works

The visualizer currently uses a set of mock temporal echo data (`src/data/mockEchoes.js`) to demonstrate its functionality. In a future iteration, it could be extended to integrate with a backend API that provides real-time data from other ApocalypsAI temporal anomaly detection utilities.

## Automated Tests

To run the automated tests:

```bash
cd react-webpage/nightly-temporal-echo-viz
npm test
```

The tests are written using `@testing-library/react` and Jest, ensuring component functionality and filtering logic work as expected. They use local mock data for deterministic and offline execution.
