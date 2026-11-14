# Nightly Temporal Tear Triage Dashboard

This utility provides a whimsical-yet-useful React web interface for visualizing and triaging detected temporal tears and anomalies. It allows users to track the status of various temporal disturbances, moving them through different triage stages like 'Detected', 'Investigating', and 'Stabilized'.

## Features

-   **Interactive Dashboard**: Drag-and-drop functionality to move temporal tears between triage columns.
-   **Clear Status Visualization**: Easily see the current state of all detected anomalies.
-   **Whimsical Theme**: Embrace the chaos of temporal distortions with a themed interface.

## Setup and Installation

To run this dashboard, you'll need Node.js and npm installed on your system.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-tear-triage-dashboard
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Start the development server**:
    ```bash
    npm start
    ```
    This will open the dashboard in your web browser, usually at `http://localhost:3000`.

## Usage

Once the dashboard is running:

-   Temporal tears will appear as cards in the 'Detected' column.
-   Click and drag a tear card to move it to another column ('Investigating' or 'Stabilized') to update its status.
-   The dashboard provides a simple, visual way to manage your temporal anomaly backlog.

## Running Tests

To ensure the dashboard's functionality is intact, you can run the automated tests:

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-tear-triage-dashboard
    ```

2.  **Run the tests**:
    ```bash
    npm test
    ```
    This will execute the Jest tests and report the results in your terminal.
