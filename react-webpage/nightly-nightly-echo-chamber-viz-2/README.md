# Nightly Echo Chamber Visualizer

## Summary
This utility provides an interactive React web interface to visualize recurring temporal patterns and 'data echoes' from various community logs or event streams. It helps identify trends, anomalies, or historical recurrences in a user-friendly, filterable timeline view.

## Features
- Displays a list of 'echoes' with timestamps, categories, and descriptions.
- Allows filtering echoes by a search term.
- Simple, clean interface for quick insights.

## Setup and Installation
1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-echo-chamber-viz
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run the application in development mode:**
    ```bash
    npm start
    ```
    This will open the application in your browser (usually `http://localhost:3000`).

4.  **Build for production:**
    ```bash
    npm run build
    ```
    This creates a `build` directory with optimized static files.

## Usage
Upon launching, the application will display a list of pre-loaded or mocked temporal echoes. You can:
- **Browse the echoes:** Each echo shows its timestamp, category, and a brief description.
- **Filter echoes:** Use the search bar at the top to filter echoes by any text contained in their category or description.

## Data Format
The application expects an array of JSON objects, each representing a 'temporal echo'. The structure should be as follows:

```json
[
  {
    "id": "unique-id-1",
    "timestamp": "2023-10-26T10:00:00Z",
    "category": "Anomaly",
    "description": "Minor temporal ripple detected near Sector 7G."
  },
  {
    "id": "unique-id-2",
    "timestamp": "2023-10-25T14:30:00Z",
    "category": "Resource Fluctuation",
    "description": "Unusual spike in 'Scrap Metal' readings in the Western Wastes."
  },
  {
    "id": "unique-id-3",
    "timestamp": "2023-10-26T08:15:00Z",
    "category": "Communication Intercept",
    "description": "Repeated distress signal pattern from unknown origin."
  }
]
```

For demonstration purposes, initial data is hardcoded in `src/App.js`. In a real-world scenario, this could be fetched from an API or loaded from a local JSON file.
