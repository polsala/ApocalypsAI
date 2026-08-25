# Nightly Temporal Echo Visualizer (nightly-temporal-echo-viz)

An interactive React web application designed to help the community detect and visualize recurring temporal patterns, or "echoes," within timestamped event data. Whether you're tracking anomaly sightings, resource drops, or community morale shifts, this tool helps you uncover hidden rhythms.

## Features

*   **Data Input**: Easily paste JSON data containing timestamped events.
*   **Timeline Visualization**: See your events laid out chronologically.
*   **Echo Detection**: Highlights recurring intervals for specific event types.
*   **Interactive**: Filter events, zoom the timeline (basic).

## Data Format

The application expects a JSON array of objects, each with a `timestamp` (ISO 8601 string) and an `event` (string) field.

```json
[
  {"timestamp": "2024-01-01T10:00:00Z", "event": "Strange light in Sector 7"},
  {"timestamp": "2024-01-04T10:00:00Z", "event": "Strange light in Sector 7"},
  {"timestamp": "2024-01-02T14:30:00Z", "event": "Ration pack discovered"},
  {"timestamp": "2024-01-09T14:30:00Z", "event": "Ration pack discovered"},
  {"timestamp": "2024-01-05T08:00:00Z", "event": "Community morale low"}
]
```

## Setup and Running

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-temporal-echo-viz
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Start the development server**:
    ```bash
    npm start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

## Running Tests

```bash
npm test
```

## Technologies Used

*   React
*   JavaScript (ES6+)
*   CSS
*   `date-fns` for date manipulation
