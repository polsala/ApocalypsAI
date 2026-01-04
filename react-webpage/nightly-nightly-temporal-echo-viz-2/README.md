# Nightly Temporal Echo Visualizer (nightly-temporal-echo-viz)

An interactive React web interface designed to provide a whimsical-yet-critical visualization of temporal anomalies, echo patterns, and distortion stability within the ApocalypsAI network. Keep an eye on the fabric of spacetime!

## Features

*   **Temporal Distortion Graph:** Visualize the severity of temporal distortions over a timeline.
*   **Echo Intensity Monitor:** Track the strength of temporal echoes, indicating potential feedback loops.
*   **Stability Index:** A calculated metric to gauge the overall temporal stability.
*   **Retro-Futuristic UI:** A charming interface reminiscent of pre-apocalyptic diagnostic tools.
*   **Real-time (Simulated) Data:** Displays dynamically updating data for continuous monitoring.

## Installation

This utility is a standalone React application.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-temporal-echo-viz
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    # or
    yarn install
    ```

## Usage

To run the development server and view the visualizer:

```bash
npm start
# or
yarn start
```

This will typically open the application in your browser at `http://localhost:3000`.

To build the production-ready static files:

```bash
npm run build
# or
yarn build
```

The built files will be located in the `build/` directory, ready for deployment on any static web server.

## Development

The project was bootstrapped with Create React App.

*   `npm start`: Runs the app in development mode.
*   `npm test`: Launches the test runner.
*   `npm run build`: Builds the app for production.
*   `npm run eject`: Ejects the Create React App configuration (use with caution).

## Tests

Tests are implemented using Jest and React Testing Library. They ensure components render correctly and interact as expected with mock data.
