# Nightly Temporal Echo Visualizer

## Summary

This utility provides an interactive React web application to visualize "temporal echoes" – significant events, utility generations, or simulated anomalies – on a dynamic timeline. It helps the community understand the flow of project activity and observe patterns or anomalies over time.

## Features

*   **Dynamic Timeline**: Scrollable and zoomable (conceptually, for this basic version, it's a list) display of events.
*   **Event Details**: Clickable events to reveal more information.
*   **Simulated Echoes**: Demonstrates how to integrate various types of temporal data.

## Setup and Running

To run this application, you will need Node.js and npm (or yarn) installed.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-temporal-echo-viz
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

    This will typically open the application in your browser at `http://localhost:3000`.

## Usage

The application will display a timeline of simulated temporal echoes. Each echo represents an event with a date, title, description, and type. You can interact with the timeline to view details of each event.

## Development

*   **`src/App.jsx`**: The main application component, responsible for fetching (simulated) data and rendering the `Timeline`.
*   **`src/components/Timeline.jsx`**: Renders the list of `EchoEvent` components.
*   **`src/components/EchoEvent.jsx`**: Displays individual event details.
*   **`src/index.jsx`**: Entry point for the React application.
*   **`src/index.html`**: The base HTML file.
*   **`src/App.css`**: Basic styling for the application.

## Testing

To run the automated tests:

```bash
npm test
# or yarn test
```

Tests are located in the `tests/` directory and use `@testing-library/react` and Jest.
