# Nightly Temporal Echo Visualization Dashboard (nightly-temporal-echo-viz)

An interactive React web dashboard designed to help the community visualize detected temporal echoes and their potential impact zones. This tool provides a clear, map-based interface to understand where temporal anomalies are most active, aiding in safe navigation and resource planning in the post-apocalyptic landscape.

## Features

*   **Interactive Map**: Displays temporal echoes as shimmering, fading circles on a customizable map.
*   **Echo Details**: Click on an echo to view its intensity, timestamp, and a whimsical description of the temporal distortion.
*   **Simulated Data**: Comes pre-loaded with mock temporal echo data for demonstration and offline use.
*   **Impact Radius Visualization**: Echoes are rendered with a radius proportional to their intensity, indicating potential areas of temporal instability.

## Installation

To get this dashboard up and running, ensure you have Node.js and npm installed.

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/react-webpage/nightly-temporal-echo-viz
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```

## Usage

To start the development server and view the dashboard in your browser:

```bash
npm start
```

This will open the application in your default web browser, usually at `http://localhost:3000`.

## Testing

To run the automated tests for the dashboard components and utilities:

```bash
npm test
```

Tests are designed to be deterministic and run offline, using mocked data and `react-leaflet` components.

## Mock Rationale for Tests

*   `src/data/mockEchoData.js`: Provides a static, consistent dataset for all tests, ensuring predictable outcomes without relying on external data sources or random generation.
*   `react-leaflet` components (`MapContainer`, `TileLayer`, `Marker`, `Popup`, `Circle`): These components are mocked in `tests/EchoMap.test.js` to prevent actual map rendering, network requests for map tiles, and browser-specific rendering issues. This allows tests to focus purely on the React component logic, prop passing, and event handling in an isolated, deterministic environment.
