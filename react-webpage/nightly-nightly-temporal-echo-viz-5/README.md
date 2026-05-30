# Nightly Temporal Echo Visualizer (Nightly-Temporal-Echo-Viz)

An interactive React web application designed to help the community visualize and understand temporal anomalies and their "echoes" on a dynamic timeline. This tool provides a clear, chronological representation of distortions, aiding in analysis and response.

## Features

*   **Dynamic Timeline**: Visualize anomalies based on their timestamp.
*   **Echo Effects**: Subtle visual cues to represent the "echo" or lingering effects of temporal distortions.
*   **Anomaly Details**: Clickable points on the timeline to reveal more information about each anomaly.
*   **Simple Input**: Easily add new anomalies for tracking and simulation.

## How to Run

This utility is a standard React application.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-temporal-echo-viz
    ```

2.  **Install dependencies**:
    ```bash
    npm install # or yarn install
    ```

3.  **Start the development server**:
    ```bash
    npm start # or yarn start
    ```
    This will typically open the application in your browser at `http://localhost:3000`.

4.  **Build for production**:
    ```bash
    npm run build # or yarn build
    ```
    This will create a `build/` directory with the static assets.

## How to Use

The application presents a timeline. You can add new temporal anomalies using the input form provided. Each anomaly requires:

*   **Timestamp**: The exact moment the anomaly was observed (e.g., `2024-07-20T14:30:00Z`).
*   **Description**: A brief explanation of the anomaly (e.g., "Minor time loop in sector Gamma-7").
*   **Severity**: A numerical value (1-5) indicating the impact or intensity.

Anomalies will appear on the timeline, with higher severity potentially having more pronounced echo effects.

## Project Structure

```
.
├── README.md
├── public/
│   └── index.html      # Main HTML file
├── src/
│   ├── App.jsx         # Main React application component
│   ├── index.jsx       # React entry point
│   ├── styles/
│   │   └── App.css     # Global styles
│   └── components/
│       └── AnomalyTimeline.jsx # Component for rendering the timeline
└── tests/
    └── App.test.jsx    # Automated tests for the application
```
