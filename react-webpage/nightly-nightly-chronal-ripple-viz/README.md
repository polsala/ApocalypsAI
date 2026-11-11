# nightly-chronal-ripple-viz

An interactive React web application to visualize simulated chronal ripples and temporal distortions. This utility provides a dynamic interface to observe and manipulate parameters of hypothetical temporal phenomena, offering a whimsical yet insightful glimpse into the fabric of spacetime.

## Features

*   **Adjustable Parameters**: Control ripple count, speed, decay rate, and color scheme.
*   **Dynamic Visualization**: Watch chronal ripples expand and fade on a canvas.
*   **Interactive Controls**: Trigger new ripples manually or observe continuous generation.

## Installation

To set up and run the Chronal Ripple Visualizer locally:

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-chronal-ripple-viz
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

## Usage

1.  **Start the development server**:
    ```bash
    npm start
    ```
    This will open the application in your browser (usually `http://localhost:3000`).

2.  **Interact with the UI**:
    *   Use the sliders and input fields to adjust parameters like "Ripple Count", "Ripple Speed", and "Ripple Decay".
    *   Click the "Generate Ripple" button to create a new ripple instantly.
    *   Observe the canvas for the dynamic visualization of chronal ripples.

## Project Structure

```
.
├── README.md
├── package.json
├── public/
│   └── index.html         # Main HTML entry point
├── src/
│   ├── App.jsx            # Main React component, handles state and controls
│   ├── RippleCanvas.jsx   # Canvas component for drawing ripples
│   ├── index.jsx          # React application entry point
│   └── styles.css         # Basic styling
└── tests/
    └── App.test.jsx       # Automated tests for React components
```

## Automated Tests

To run the automated tests for this utility:

```bash
npm test
```

The tests use `Jest` and `@testing-testing-library/react` to ensure component rendering, interaction, and proper canvas API calls (via mocks).
