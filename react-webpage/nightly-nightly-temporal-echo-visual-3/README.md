# Nightly Temporal Echo Visualizer

## Summary
This utility provides an interactive React web application designed to visualize subtle temporal echoes and distortions. It presents a dynamic, evolving pattern on a grid, where each point's 'echo strength' fluctuates over time, offering a whimsical yet insightful glance into the fabric of spacetime anomalies.

## Features
*   **Dynamic Grid Visualization**: A grid of points whose properties (size, color) change based on simulated temporal echo data.
*   **Real-time Simulation**: Echoes propagate and decay, creating mesmerizing patterns.
*   **React-based**: Modern, component-driven architecture for easy extension.

## Installation
1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/react-webpage/nightly-temporal-echo-visualizer
    ```
2.  **Ensure Node.js and npm are installed.**
3.  **Install project dependencies:**
    ```bash
    npm install
    ```

## Usage
To start the development server and view the visualizer in your browser:
```bash
npm start
```
This will typically open the application at `http://localhost:3000`.

To build a production-ready static application:
```bash
npm run build
```
The built files will be located in the `build/` directory.

## Development
*   The main application logic resides in `src/App.jsx` and `src/components/EchoVisualizer.jsx`.
*   Styling is in `src/styles/App.css`.
*   Feel free to modify the `EchoVisualizer` component to experiment with different patterns, colors, and echo behaviors.

## Tests
To run the automated tests for the visualizer:
```bash
npm test
```
Tests are located in `tests/EchoVisualizer.test.jsx` and ensure the component renders correctly and updates its state as expected over simulated time.
