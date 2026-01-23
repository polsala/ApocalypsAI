# Nightly Wasteland Trade Map

## Summary

The `nightly-wasteland-trade-map` is an interactive React web application designed to help survivors visualize critical resource locations across the desolate wasteland and plan the most optimal (and safest!) trade routes between them. It incorporates whimsical risk factors like 'Mutant Infestations' and 'Sandstorm Alleys' into its pathfinding algorithm, making trade decisions a delightful challenge.

## Features

*   **Interactive Map:** A simple grid-based map where users can mark resource locations.
*   **Resource Management:** Add, name, and remove resource locations.
*   **Route Planning:** Select a start and end point to calculate the 'safest' (lowest cost) route.
*   **Whimsical Risk Factors:** Predefined zones or path segments with varying 'costs' representing dangers or opportunities (e.g., high cost for 'Mutant Infestation', low cost for 'Oasis Respite').
*   **Visual Feedback:** Routes are drawn directly on the map.

## How to Run

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-wasteland-trade-map
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

1.  **Add Resource Locations:** Click on any grid cell on the map to add a new resource location. You'll be prompted to name it.
2.  **Select Start/End Points:** Use the dropdowns in the 'Route Planner' panel to select your desired starting and ending resource locations.
3.  **Calculate Route:** Click the 'Calculate Route' button to see the optimal path highlighted on the map, along with its total 'risk cost'.
4.  **Remove Locations:** Click on an existing resource marker to remove it.

## Development Notes

The map is a simplified SVG grid. Pathfinding uses a basic Dijkstra's algorithm, where edge weights are influenced by hardcoded 'risk zones' on the map. This utility is designed for local use and does not persist data.
