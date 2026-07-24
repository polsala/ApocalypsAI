# Nightly Whisperscape Weaver

An interactive web application for the ApocalypsAI community to share and visualize "whispers" – short, ephemeral messages, observations, or survival tips. As whispers are added, they form a dynamic, interconnected "whisperscape" on the screen, reflecting the collective consciousness of the wasteland.

## Features

- **Whisper Input**: Easily submit new whispers.
- **Dynamic Visualization**: See whispers appear and subtly interact on a canvas. (Initial version: simple list/tag cloud, future: force-directed graph).
- **Local Persistence**: Whispers are saved in your browser's local storage.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-whisperscape-weaver
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

## How to Use

1.  Type your "whisper" into the input field.
2.  Click "Weave Whisper" to add it to the whisperscape.
3.  Observe the whispers appearing on the canvas. They are saved locally, so they'll persist even if you close and reopen the tab.

## Project Structure

```
.
├── public/
│   └── index.html      # Standard React HTML template
├── src/
│   ├── App.js          # Main application component
│   ├── App.css         # Main application styles
│   ├── index.js        # React entry point
│   ├── index.css       # Global styles
│   ├── components/
│   │   ├── WhisperInput.js     # Component for inputting whispers
│   │   └── WhisperscapeCanvas.js # Component for displaying whispers
├── package.json        # Project dependencies and scripts
└── README.md           # This file
```

## Automated Tests

To run the tests:

```bash
cd react-webpage/nightly-whisperscape-weaver
npm test
```

Tests cover component rendering and basic interaction.
