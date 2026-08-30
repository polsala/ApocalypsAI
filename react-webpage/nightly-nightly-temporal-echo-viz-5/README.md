# Nightly Temporal Echo Visualizer (nightly-temporal-echo-viz)

An interactive React web application designed to visualize simulated temporal echoes and their distortion patterns across a conceptual timeline. This tool helps temporal analysts and curious survivors understand the subtle ripples and anomalies in the fabric of spacetime, without requiring direct access to a live temporal anomaly detector.

## Features

*   Input a "temporal coordinate" (e.g., a date, event, or conceptual point in time).
*   Generate a simulated set of temporal echoes with varying intensity and distortion types.
*   Visualize these echoes on a simple timeline, showing their relative positions and characteristics.
*   Whimsical and informative, aiding in the theoretical understanding of temporal phenomena.

## How to Run

1.  **Prerequisites**: Ensure Node.js and npm (or yarn) are installed.
2.  **Navigate**: Change directory into `nightly-temporal-echo-viz`.
3.  **Install Dependencies**:
    ```bash
    npm install
    # or yarn install
    ```
4.  **Start Development Server**:
    ```bash
    npm start
    # or yarn start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

## How to Use

1.  Enter a descriptive "Temporal Coordinate" in the input field (e.g., "The Great Silence", "Epoch of Rust", "2077-10-23 04:00 UTC").
2.  Click the "Generate Echoes" button.
3.  Observe the simulated temporal echoes displayed on the timeline below. Each echo will be represented by a colored bar or point, with its length or intensity indicating its strength, and color indicating its distortion type.

## Project Structure

```
.
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   ├── components/
│   │   └── EchoVisualizer.js
│   └── components/
│       └── EchoVisualizer.css
└── tests/
    └── EchoVisualizer.test.js
```

## Automated Tests

To run the tests:

```bash
npm test
# or yarn test
```

Tests are written using React Testing Library and Jest, ensuring the core components function as expected.
