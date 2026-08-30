# Nightly Temporal Echo Visualizer (nightly-temporal-echo-viz)

An interactive React web application designed to visualize temporal echoes and anomalies detected across the ApocalypsAI network. This tool provides a dynamic timeline view, allowing community members to observe patterns, magnitudes, and types of temporal distortions.

## Features

*   **Dynamic Timeline:** Visualize temporal events chronologically.
*   **Echo Details:** Click on an echo to view its timestamp, type, and magnitude.
*   **Whimsical UI:** A retro-futuristic interface with subtle glitch effects to match the temporal theme.
*   **Self-contained:** Runs locally with sample data or can be adapted to consume real-time feeds.

## Installation and Usage

This utility requires Node.js and npm (or yarn) to run.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-temporal-echo-viz
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    # or yarn install
    ```

3.  **Run the application:**
    ```bash
    npm start
    # or yarn start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

## Data Format

The application expects a JSON array of temporal echo objects, each with the following structure:

```json
[
  {
    "id": "unique-echo-id-1",
    "timestamp": "ISO 8601 string (e.g., 2024-07-21T10:30:00Z)",
    "type": "Temporal Shift",
    "magnitude": 0.75,
    "description": "Minor localized time dilation detected near Sector Gamma."
  },
  {
    "id": "unique-echo-id-2",
    "timestamp": "2024-07-21T11:15:00Z",
    "type": "Causal Loop",
    "magnitude": 1.2,
    "description": "Small causal loop identified, self-correcting within minutes."
  }
]
```

The sample data (`src/data/sample-echoes.json`) follows this format.

## Development

The project was bootstrapped with Create React App.

*   `npm start`: Runs the app in development mode.
*   `npm test`: Launches the test runner.
*   `npm run build`: Builds the app for production.

## Tests

Tests are implemented using React Testing Library and Jest. They ensure the main application component renders correctly and processes data as expected.
