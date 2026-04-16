# Nightly Temporal Echo Visualizer

## Overview

The `nightly-temporal-echo-visualizer` is a whimsical-yet-useful React web application designed to provide an interactive dashboard for visualizing temporal echoes and anomalies detected by various ApocalypsAI monitoring agents. It helps the community understand the patterns, severity, and locations of temporal distortions in a user-friendly, visual format.

## Features

*   **Interactive Timeline/Grid**: Displays temporal echoes as visual elements on a dynamic canvas.
*   **Echo Details Panel**: Click on an echo to view its detailed information, including timestamp, location, severity, and type.
*   **Whimsical Visuals**: Each echo type might have a distinct visual representation or animation.
*   **Mock Data**: Comes pre-loaded with mock data for demonstration and testing purposes.

## Setup and Installation

To run this utility, you need Node.js and npm (or yarn) installed.

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
    This will open the application in your browser, usually at `http://localhost:3000`.

4.  **Build for production (optional)**:
    ```bash
    npm run build
    # or yarn build
    ```
    This creates a `build` directory with the production-ready static files.

## Running Tests

To run the automated tests for this utility:

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-temporal-echo-visualizer
    ```

2.  **Run the test command**:
    ```bash
    npm test
    # or yarn test
    ```
    This will execute the tests using Jest and React Testing Library.

## Contributing

Feel free to expand upon the visualization types, add filtering capabilities, or integrate with actual ApocalypsAI data sources (once available!).
