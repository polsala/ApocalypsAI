# Nightly Temporal Echo Visualizer (nightly-temporal-echo-viz)

An interactive React web interface to visualize detected temporal echoes and their perceived "intensity" and "origin" over a timeline.

## Summary

This utility provides a whimsical yet insightful web dashboard for ApocalypsAI community members to explore temporal anomalies, affectionately termed "echoes." It allows users to visualize these echoes on a timeline, filter them by intensity and perceived origin (Past, Future, Alternate Reality), and view detailed descriptions. This helps in understanding the temporal landscape, identifying patterns, and prioritizing investigations into spacetime distortions.

## Features

*   **Interactive Timeline:** See temporal echoes plotted chronologically.
*   **Filter Options:** Easily filter echoes by their intensity (1-5) and origin category.
*   **Detailed Echo Cards:** Click on an echo to reveal its full description and properties.
*   **Whimsical Descriptions:** Each echo comes with a unique, often humorous, description of its perceived manifestation.

## Usage

To run this utility:

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-temporal-echo-viz
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

## Development & Testing

The application uses standard React development practices.

### Running Tests

```bash
npm test
```

## Mock Rationale

The application uses `src/data/mockEchoes.js` as its data source. This ensures that the utility is fully self-contained, deterministic, and can be run and tested offline without requiring any external API calls or complex setup. The mock data simulates various temporal echoes with different intensities, origins, and descriptions for demonstration and testing purposes.
