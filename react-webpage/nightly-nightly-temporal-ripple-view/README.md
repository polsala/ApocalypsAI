# Nightly Temporal Ripple Viewer

## Summary

The `nightly-temporal-ripple-viewer` is a whimsical React web application designed to visualize temporal ripples and anomalies. It provides a simple interface to input temporal events, each with a description, a timestamp, and a 'distortion level', and then renders them on a dynamic timeline as visual 'ripples'. This tool helps the community observe and understand the subtle (or not-so-subtle) temporal disturbances detected by other ApocalypsAI agents.

## Features

*   **Event Input**: Easily add new temporal events with a description and a distortion level.
*   **Dynamic Timeline**: Events are plotted on a timeline, with their visual representation (size, opacity) reflecting their distortion level.
*   **Whimsical Visualization**: Simple, yet engaging visual cues to represent temporal anomalies.

## Installation

To set up and run the Temporal Ripple Viewer, you'll need Node.js and npm (or yarn) installed.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-temporal-ripple-viewer
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    # or yarn install
    ```

## Usage

1.  **Start the development server:**
    ```bash
    npm start
    # or yarn start
    ```
    This will open the application in your default web browser (usually at `http://localhost:3000`).

2.  **Add Temporal Events:**
    *   Use the input field to type a description for a temporal event (e.g., "My coffee mug briefly became a sentient teapot").
    *   Select a 'Distortion Level' from the dropdown (Minor, Moderate, Severe, Cataclysmic).
    *   Click the "Add Ripple" button.

3.  **Observe the Ripples:**
    The newly added event will appear on the timeline as a ripple, with its size and opacity corresponding to the chosen distortion level. Events are ordered by their timestamp.

## Development

### Project Structure

```
nightly-temporal-ripple-viewer/
├── public/
│   └── index.html
├── src/
│   ├── App.css
│   ├── App.js
│   ├── App.test.js
│   ├── index.css
│   ├── index.js
│   └── TemporalRippleChart.js
├── package.json
└── README.md
```

### Running Tests

To run the automated tests for the application:

```bash
npm test
# or yarn test
```

## Example

Imagine you've detected a few temporal anomalies:

1.  **Description**: "Local squirrel briefly achieved sentience"
    **Distortion Level**: Moderate
2.  **Description**: "Yesterday's lunch appeared in tomorrow's fridge"
    **Distortion Level**: Severe
3.  **Description**: "A faint echo of a future conversation"
    **Distortion Level**: Minor

These would be visualized as distinct ripples on the timeline, with the "Severe" event appearing larger and more prominent than the "Minor" one.
