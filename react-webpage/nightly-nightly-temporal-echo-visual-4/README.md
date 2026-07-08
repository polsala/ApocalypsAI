# Nightly Temporal Echo Visualizer

## Summary

This utility provides an interactive React web interface to visualize a sequence of temporal events, helping to identify patterns, 'echoes', and propagation over time. It's designed for the ApocalypsAI community to gain insights into event sequences, system logs, or any time-series data that might reveal hidden temporal relationships.

## Features

*   **Event Timeline:** Displays events chronologically on an interactive timeline.
*   **Detailed Event Cards:** Each event can be expanded to show its full data payload.
*   **JSON Input:** Easily paste raw JSON event data into the interface.
*   **Whimsical UI:** A dark, sci-fi themed interface fitting the ApocalypsAI aesthetic.

## Installation & Setup

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-temporal-echo-visualizer
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```

## Usage

1.  **Start the development server:**
    ```bash
    npm start
    ```
    This will open the application in your browser (usually `http://localhost:3000`).

2.  **Input Event Data:**
    On the webpage, you will find a text area. Paste your event data as a JSON array into this area. Each event object should have at least `id`, `timestamp`, and `type` fields. Additional fields will be displayed in the event details.

    **Example Event Data Format:**
    ```json
    [
      { "id": "e001", "timestamp": "2024-01-01T08:00:00Z", "type": "SensorRead", "value": 22.5, "unit": "C" },
      { "id": "e002", "timestamp": "2024-01-01T08:05:30Z", "type": "SystemAlert", "severity": "Warning", "message": "Temperature rising" },
      { "id": "e003", "timestamp": "2024-01-01T08:10:15Z", "type": "ActionTaken", "action": "InitiateCooling", "target": "ZoneAlpha" },
      { "id": "e004", "timestamp": "2024-01-01T08:12:00Z", "type": "SensorRead", "value": 23.1, "unit": "C" },
      { "id": "e005", "timestamp": "2024-01-01T08:15:45Z", "type": "SystemAlert", "severity": "Critical", "message": "Cooling system unresponsive" },
      { "id": "e006", "timestamp": "2024-01-01T08:20:00Z", "type": "ManualIntervention", "user": "ApocalypsAI-07", "details": "Override cooling system" }
    ]
    ```

3.  **Visualize:**
    Click the "Load Events" button. The events will be rendered on a timeline, ordered by their timestamps. Click on individual event cards to expand and view their full JSON data.

## Development

To build the production-ready static files:

```bash
npm run build
```

The built files will be located in the `build/` directory.

## Tests

To run the automated tests:

```bash
npm test
```
