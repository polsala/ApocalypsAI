# Nightly Temporal Ripple Viewer

An interactive React web interface designed to visualize and monitor detected temporal ripples and anomalies across the ApocalypsAI network. This utility provides a whimsical yet functional dashboard to observe the "temporal fabric" and track its stability.

## Features

*   **Ripple Visualization**: See active temporal anomalies displayed as interactive cards.
*   **Severity Indicators**: Quickly identify the impact level of each ripple.
*   **Stabilization Control**: Mark anomalies as "stabilized" to track resolution efforts.
*   **Offline Ready**: Uses mock data for development and demonstration, no backend required.

## Installation and Setup

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-temporal-ripple-viewer
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    # or
    yarn install
    ```

3.  **Start the development server**:
    ```bash
    npm start
    # or
    yarn start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

4.  **Build for production (optional)**:
    ```bash
    npm run build
    # or
    yarn build
    ```
    This creates a `build` directory with the production-ready static files.

## Usage

The web interface will display a dashboard of temporal anomalies. Each anomaly is represented by a card showing its type, severity, and timestamp. Click the "Stabilize" button on a ripple card to mark it as resolved. The dashboard will update to reflect the change.

## Mock Data

The application uses `src/api/mockTemporalData.js` to simulate real-time anomaly data. This allows the viewer to function completely offline and provides a consistent dataset for testing and demonstration purposes. In a real-world scenario, this data would be fetched from an ApocalypsAI anomaly detection service.
