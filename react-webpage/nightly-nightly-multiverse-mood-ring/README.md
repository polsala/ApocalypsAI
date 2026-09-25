# Nightly Multiverse Mood Ring

## Overview

The `nightly-multiverse-mood-ring` is a whimsical-yet-useful React web application designed to provide a quick, visual overview of the 'mood' or status of various ApocalypsAI system components or detected temporal anomalies. It uses color and subtle animations to represent different states, offering an intuitive glance at the cosmic vibes of our operations.

## Features

*   **Dynamic Mood Visualization**: Displays several 'mood rings', each representing a different aspect (e.g., Temporal Stability, Agent Activity, Resource Flux).
*   **Color-Coded Status**: Each mood ring changes color based on its status (Stable, Fluctuating, Anomalous, Unknown).
*   **Animated Indicators**: Subtle CSS animations (pulse, glitch, calm) provide additional visual cues for the current state.
*   **Interactive Refresh**: A button allows users to refresh the displayed moods, simulating new data or a system check.

## Installation and Setup

To run this utility, you'll need Node.js and npm (or yarn) installed on your system.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-multiverse-mood-ring
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```

3.  **Start the development server**:
    ```bash
    npm start
    # or yarn start
    ```
    This will open the application in your default web browser, usually at `http://localhost:3000`.

## Usage

Once the application is running:

*   Observe the mood rings, each displaying a name (e.g., "Temporal Stability") and its current status (e.g., "Stable", "Anomalous").
*   The color and animation of each ring will reflect its status:
    *   **Stable (Green)**: Calm, steady state.
    *   **Fluctuating (Yellow)**: Pulsing, indicating minor changes or uncertainty.
    *   **Anomalous (Red)**: Glitching, suggesting a significant deviation or issue.
    *   **Unknown (Grey)**: Static, indicating data unavailability or an unmonitored state.
*   Click the "Refresh Multiverse Vibes" button to generate new, random moods for all rings, simulating an update.

## Project Structure

```
nightly-multiverse-mood-ring/
├── public/
│   └── index.html          # Main HTML file
├── src/
│   ├── App.css             # Global styles for the application
│   ├── App.js              # Main React application component
│   ├── index.css           # Base CSS for the React app
│   ├── index.js            # React entry point
│   ├── MoodRing.css        # Styles specific to the MoodRing component
│   └── MoodRing.js         # Reusable MoodRing component
├── tests/
│   └── App.test.js         # Automated tests for the App component
└── package.json            # Project dependencies and scripts
```

## Testing

To run the automated tests for this utility:

```bash
cd react-webpage/nightly-multiverse-mood-ring
npm test
# or yarn test
```

The tests are deterministic and offline, using Jest and React Testing Library. `Math.random()` is mocked to ensure predictable mood generation during testing.
