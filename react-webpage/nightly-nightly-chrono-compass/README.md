# Nightly Chrono-Compass

An interactive React web application designed to visualize temporal stability across simulated regions and provide actionable suggestions for drift correction. This tool helps the community monitor the subtle (and not-so-subtle) temporal anomalies that plague our post-apocalyptic existence, ensuring our timelines remain as coherent as possible.

## Features

*   **Temporal Stability Map**: A visual representation of various regions, color-coded by their temporal stability.
*   **Drift Visualization**: Regions with higher temporal drift are visually emphasized.
*   **Interactive Selection**: Click on any region to view detailed stability metrics and receive tailored correction suggestions.
*   **Correction Protocols**: Provides whimsical-yet-actionable advice based on the severity of temporal drift.

## How to Run

This utility is a standard Create React App project.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-chrono-compass
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Start the development server**:
    ```bash
    npm start
    ```
    This will open the application in your browser (usually `http://localhost:3000`).

4.  **Build for production (optional)**:
    ```bash
    npm run build
    ```
    This creates a `build` directory with the production-ready static files.

## How to Test

To run the automated tests for this utility:

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-chrono-compass
    ```

2.  **Run tests**:
    ```bash
    npm test -- --watchAll=false
    ```
    The `--watchAll=false` flag ensures the tests run once and exit, suitable for CI/CD environments.

## Project Structure

```
.
├── public/
│   └── index.html          # Main HTML template
├── src/
│   ├── components/
│   │   ├── ChronoMap.js    # SVG-based temporal map visualization
│   │   └── CorrectionSuggestions.js # Displays detailed region info and suggestions
│   ├── App.js              # Main application component, handles data and state
│   └── index.js            # React entry point
├── tests/
│   ├── App.test.js         # Tests for the main App component
│   └── ChronoMap.test.js   # Tests for the ChronoMap visualization component
├── package.json            # Project dependencies and scripts
└── README.md               # This file
```
