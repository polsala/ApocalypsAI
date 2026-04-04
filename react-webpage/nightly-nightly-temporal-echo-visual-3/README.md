# Nightly Temporal Echo Visualizer

## Summary

This utility provides a whimsical-yet-useful interactive React web interface to visualize detected temporal echoes and anomalies. It's designed to give the community a user-friendly dashboard to observe spacetime distortions, helping to understand their patterns and magnitudes over time.

## Features

*   **Interactive Display**: View temporal echoes as a list of events.
*   **Simulated Data**: Comes with mock data to demonstrate functionality out-of-the-box.
*   **Extensible**: Easily adaptable to consume real-time data from other ApocalypsAI temporal utilities.

## Installation & Setup

1.  **Navigate to the utility directory**:
    ```bash
    cd nightly-temporal-echo-visualizer
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

## Usage

The web interface will display a list of detected temporal echoes, each with a timestamp, magnitude, and type. The current version uses simulated data. To integrate with actual temporal anomaly detection utilities, you would modify `src/App.js` to fetch data from your desired source.

### Data Format Expectation

The `App.js` component expects an array of objects, each representing a temporal echo, with the following structure:

```javascript
[
  {
    id: 'unique-id-1',
    timestamp: '2024-07-20T10:00:00Z',
    magnitude: 0.75,
    type: 'Minor Ripple',
    description: 'A slight tremor in the fabric of time.'
  },
  // ... more echoes
]
```

## Development

*   **`src/App.js`**: Main application component, manages data and renders the display.
*   **`src/TemporalEchoDisplay.js`**: Component responsible for rendering the list of echoes.
*   **`src/App.css`**: Basic styling for the application.

## Running Tests

To run the automated tests, use:

```bash
npm test
```
