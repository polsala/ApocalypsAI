# Nightly Workflow Weaver

## Overview

The `nightly-workflow-weaver` is a whimsical React web application designed to visualize the ApocalypsAI's nightly GitHub Actions workflow runs. It presents the various agents and their recent activities as interconnected 'nodes' in a 'cosmic loom', offering a quick, at-a-glance understanding of the system's health and 'mood'.

Each workflow node displays its name, current status (success, failure, running), and a randomly assigned whimsical 'mood' emoji, making the monitoring process a bit more enchanting.

## Features

*   **Whimsical Visualization**: Workflows are represented as nodes with unique 'moods'.
*   **Status Indicators**: Clear visual cues for workflow success, failure, or ongoing execution.
*   **Interactive**: (Future enhancement: clickable nodes for more details, filtering).
*   **Mock Data**: Uses mock API calls for deterministic, offline testing and easy local development.

## How to Run Locally

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-workflow-weaver
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Start the development server:**
    ```bash
    npm start
    ```

    This will open the application in your browser, usually at `http://localhost:3000`.

## Project Structure

```
nightly-workflow-weaver/
├── public/
│   └── index.html
├── src/
│   ├── api.js             # Mock API for workflow data
│   ├── App.js             # Main application component
│   ├── index.css          # Global styles
│   ├── index.js           # Entry point
│   ├── WorkflowGraph.js   # Component to render the collection of workflow nodes
│   └── WorkflowNode.js    # Component for a single workflow visualization
├── tests/
│   ├── api.test.js
│   ├── App.test.js
│   └── WorkflowNode.test.js
└── package.json
```

## Development Notes

*   The 'mood' of each workflow is randomly generated upon data fetch for added whimsy. In a real-world scenario, this could be derived from metrics like run duration, resource usage, or historical success rates.
*   Connections between nodes in the 'cosmic loom' are currently implied by layout and subtle visual cues. Future iterations could include dynamic SVG lines or a more sophisticated graph visualization library.
