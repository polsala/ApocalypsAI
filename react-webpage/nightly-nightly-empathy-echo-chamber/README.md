# Nightly Empathy Echo Chamber

A React-based web utility designed to help the community gauge and visualize the emotional resonance of their thoughts and communications. Input any text, and the Echo Chamber will reflect its perceived sentiment through a whimsical display of colors and shapes, encouraging self-awareness and collective empathy.

## Features

*   **Text Input**: Easily enter any message, log entry, or thought.
*   **Sentiment Echo**: Receive a visual representation (color, shape, simple animation) of the text's emotional tone.
*   **Whimsical Feedback**: Provides a lighthearted yet insightful perspective on emotional states.
*   **Local & Offline**: Runs entirely in your browser after initial build, no external APIs needed for sentiment analysis (it's a local, simplified interpretation).

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-empathy-echo-chamber
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

4.  **Build for production (optional)**:
    ```bash
    npm run build
    ```
    This creates a `build` directory with the static files ready for deployment.

## How to Use

1.  Open the application in your web browser.
2.  Type or paste your text into the input area.
3.  Click the "Echo Sentiment" button.
4.  Observe the visual feedback in the "Empathy Echo" section. The colors and shapes will shift to reflect the interpreted emotional tone of your input.

## Development Notes

The sentiment analysis is intentionally simplified and whimsical, relying on basic keyword matching and random elements to provide a "mood ring" effect rather than deep NLP. This keeps the utility self-contained and light.
