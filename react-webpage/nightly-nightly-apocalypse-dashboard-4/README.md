A whimsical React-based dashboard to visualize the state of the ApocalypsAI project.

## Features

*   **Agent Status Overview**: See the current status of various ApocalypsAI agents.
*   **Utility Count Tracker**: Monitor the number of utilities generated across different classifiers.
*   **Workflow Health**: A playful indicator of the health of our GitHub Actions workflows.
*   **Resource Scarcity Meter**: A fun, thematic meter showing perceived resource scarcity (mocked).

## Getting Started

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```

2.  **Navigate to the utility directory**:
    ```bash
    cd utils/nightly-apocalypse-dashboard
    ```

3.  **Install dependencies**:
    ```bash
    npm install
    ```

4.  **Start the development server**:
    ```bash
    npm start
    ```

    This will open the dashboard in your browser, typically at `http://localhost:3000`.

## Development

This utility is built using React. The `src/` directory contains the main components and logic.

*   `src/App.js`: The main application component.
*   `src/components/AgentStatus.js`: Component to display agent statuses.
*   `src/components/UtilityCounter.js`: Component to display utility counts.
*   `src/components/WorkflowHealth.js`: Component for workflow health indicators.
*   `src/components/ResourceMeter.js`: Component for the resource scarcity meter.
*   `src/utils/mockData.js`: Mock data for demonstration purposes.

## Testing

Tests are located in the `tests/` directory and can be run using:

```bash
npm test
```

All tests are deterministic and use mocked data to ensure offline execution.
