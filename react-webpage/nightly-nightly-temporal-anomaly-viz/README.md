# Nightly Temporal Anomaly Visualizer

A whimsical-yet-useful React web application for the ApocalypsAI community to visualize detected temporal anomalies on an interactive timeline. Keep track of those pesky time-wobbles, echo blooms, and reality shredders!

## Features

*   **Anomaly Timeline**: View a chronological list of detected temporal anomalies.
*   **Detailed Anomaly Cards**: Click on any anomaly to reveal its type, severity, location, potential impact, and a brief description.
*   **Whimsical Severity & Impact**: Anomalies are categorized with fun, thematic labels like "Mild Wobble" or "Dinosaur in the Kitchen."
*   **"Stabilization" Button**: A purely aesthetic button to give you the illusion of control over the temporal fabric.

## Getting Started

To run this utility, you'll need Node.js and npm (or yarn) installed on your system.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-temporal-anomaly-viz
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
    This command builds the app for production to the `build` folder. It correctly bundles React in production mode and optimizes the build for the best performance.

## Usage

Once the application is running:

*   The left panel displays a list of detected temporal anomalies, sorted by timestamp.
*   Click on any anomaly in the list to view its detailed information in the right panel.
*   Marvel at the descriptions and ponder the implications of a "Paradox Puddle."
*   Feel free to click the "Attempt Stabilization" button on any anomaly card. It won't do anything to time, but it might make you feel better!

## Project Structure

```
.
├── README.md
├── package.json
├── src/
│   ├── App.js                 # Main application component
│   ├── App.css                # Styling for the main app
│   ├── index.js               # React entry point
│   ├── index.css              # Global styles
│   ├── components/
│   │   ├── AnomalyTimeline.js # Component to display the list of anomalies
│   │   ├── AnomalyTimeline.css
│   │   ├── AnomalyCard.js     # Component to display details of a single anomaly
│   │   └── AnomalyCard.css
│   └── data/
│       └── anomalies.json     # Mock data for temporal anomalies
└── tests/
    ├── App.test.js            # Tests for the main App component
    ├── AnomalyTimeline.test.js# Tests for the AnomalyTimeline component
    └── setupTests.js          # Jest setup for @testing-library/jest-dom
```

## Testing

To run the automated tests:

```bash
npm test
# or
yarn test
```

The tests are deterministic and offline, using mocked data to ensure consistent results.
