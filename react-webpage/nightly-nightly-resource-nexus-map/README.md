# Nightly Resource Nexus Map

An interactive React web application to visualize tracked wasteland resources on a dynamic map, aiding in scavenging and planning. This utility provides a visual overview of resource distribution, helping survivors identify potential scavenging routes and resource-rich areas.

## Features

*   **Interactive Map**: A grid-based map displaying various resource types at different locations.
*   **Resource Filtering**: Filter resources by type (e.g., "Water", "Food", "Scrap", "Fuel").
*   **Dynamic Legend**: Explains the symbols/colors used for different resource types.
*   **Mock Data**: Uses pre-defined, whimsical wasteland resource data for demonstration.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-resource-nexus-map
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

## How to Test

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-resource-nexus-map
    ```
2.  **Run tests**:
    ```bash
    npm test
    ```
    This will execute all tests using Jest and React Testing Library.

## Mock Rationale

The map data, including resource locations and types, is entirely mocked within the application. This ensures the utility is self-contained, deterministic, and does not require external API calls or complex geographical data processing. The "map" itself is a simplified visual representation using CSS grid/flexbox, not a real-world mapping library, to maintain offline testability and simplicity.
