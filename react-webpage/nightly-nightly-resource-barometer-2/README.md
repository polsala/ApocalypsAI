# Nightly Resource Barometer

## Overview

The Nightly Resource Barometer is a whimsical-yet-useful interactive web dashboard designed to help survivors of the apocalypse keep track of their vital resources. It features animated gauges for key resources like Hydro-Essence (Water), Sustenance Scraps (Food), Spirit Spark (Morale), Mind Mettle (Sanity), and Salvage Shards (Scrap Metal). Users can manually adjust resource levels, and the dashboard provides visual feedback, with all data persistently stored in your browser's local storage.

## Features

*   **Whimsical Gauges**: Visually appealing, color-coded gauges for each resource.
*   **Interactive Controls**: Buttons to easily increase or decrease resource levels.
*   **Persistent Storage**: Resource levels are saved in `localStorage` so your data persists across browser sessions.
*   **At-a-Glance Overview**: Quickly assess your current resource situation.

## Resources Tracked

*   **Hydro-Essence (Water)**: The fundamental liquid of life.
*   **Sustenance Scraps (Food)**: Keeps the belly full and the energy flowing.
*   **Spirit Spark (Morale)**: Essential for fending off despair and maintaining hope.
*   **Mind Mettle (Sanity)**: Guards against the whispers of the void and existential dread.
*   **Salvage Shards (Scrap Metal)**: Crucial for crafting, repairs, and general tinkering.

## How to Run

To run the Nightly Resource Barometer locally, you'll need Node.js and npm installed.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-resource-barometer
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Start the development server**:
    ```bash
    npm start
    ```

    This will open the application in your default web browser, usually at `http://localhost:3000`.

## How to Use

Simply click the `+` or `-` buttons next to each resource gauge to adjust its level. The gauge will visually update, and the new value will be automatically saved. Refreshing the page will load your last saved resource levels.

## Development

This utility is built with React. The main components are `App.jsx` (the main dashboard) and `ResourceGauge.jsx` (the reusable gauge component). Styling is handled by `App.css`.

## Testing

To run the automated tests, use the following command:

```bash
npm test
```

Tests are written using `@testing-library/react` and Jest, ensuring deterministic and offline validation of component rendering and state management, including `localStorage` interactions.
