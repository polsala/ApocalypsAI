# Nightly Temporal Echo Chamber Visualizer

An interactive React web application designed to help survivors log and visualize observed temporal anomalies, aiding in the identification of patterns and potential sources of spacetime distortions.

## Overview

In the chaotic aftermath, temporal anomalies are not just a nuisance; they're a clue. The "Temporal Echo Chamber Visualizer" provides a user-friendly interface to record these strange occurrences – from phantom historical figures to objects appearing out of time – and see them laid out. By inputting details like description, timestamp, anomaly type, and perceived "temporal energy," users can build a personal database of distortions. The tool then presents these anomalies in a simple list, allowing for quick review and pattern recognition.

## Features

*   **Anomaly Logging**: Easily add new temporal events with descriptions, timestamps, types, and energy levels.
*   **Persistent Storage**: All logged anomalies are saved locally in your browser, so your data persists across sessions.
*   **Simple Visualization**: View a chronological list of all recorded anomalies.
*   **Whimsical Interface**: Designed to make the daunting task of tracking spacetime tears a little less grim.

## Installation and Setup

To run this utility, you'll need Node.js and npm (or yarn) installed on your system.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-temporal-echo-chamber-viz
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
    This will open the application in your default web browser at `http://localhost:3000`.

4.  **Build for production (optional)**:
    ```bash
    npm run build
    # or yarn build
    ```
    This command builds the app for production to the `build` folder. It correctly bundles React in production mode and optimizes the build for the best performance.

## Usage

1.  **Add an Anomaly**: Use the "Log New Anomaly" form to input details about a temporal event you've witnessed.
    *   **Description**: A brief summary of the anomaly (e.g., "Heard a faint Roman trumpet call").
    *   **Timestamp**: When the anomaly occurred (e.g., "2024-10-27T14:30").
    *   **Type**: Categorize the anomaly (e.g., "Auditory Echo", "Visual Glitch", "Object Displacement").
    *   **Energy Level**: A subjective rating of the anomaly's intensity (1-10).
2.  **View Anomalies**: All logged anomalies will appear in the "Observed Temporal Anomalies" list below the form, ordered by timestamp.
3.  **Data Persistence**: Your anomalies are automatically saved and loaded from your browser's local storage.

## Development and Testing

To run the automated tests:

```bash
npm test
# or yarn test
```

This will launch the test runner in interactive watch mode.
