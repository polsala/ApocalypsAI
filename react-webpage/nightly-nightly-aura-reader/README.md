# Nightly Aura Reader

## Overview

The `nightly-aura-reader` is a whimsical-yet-useful web utility that allows community members to input any text (e.g., a log entry, a commit message, a daily thought, or a snippet of a temporal anomaly report) and receive a visual representation of its 'emotional aura'. Think of it as a digital mood ring for your text!

It provides a quick, intuitive glance at the underlying sentiment, helping to gauge the general 'vibe' of a message or log without deep analysis. Is the system feeling 'positive' today? Is that bug report radiating 'negative' energy? Find out with a glance!

## Features

*   **Text Input**: Enter any text you wish to analyze.
*   **Aura Visualization**: A dynamic, colored shape appears, reflecting the detected sentiment.
    *   **Positive**: Warm, inviting colors (e.g., green, yellow) and smooth, flowing shapes.
    *   **Negative**: Intense, cautionary colors (e.g., red, purple) and sharp, jagged shapes.
    *   **Neutral**: Calm, balanced colors (e.g., blue, grey) and stable, regular shapes.
*   **Simple Sentiment Analysis**: Uses a lightweight, client-side keyword-based sentiment detection.

## Installation & Usage

To run the Nightly Aura Reader locally:

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-aura-reader
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    # or yarn install
    ```

3.  **Start the development server:**
    ```bash
    npm start
    # or yarn start
    ```

    This will typically open the application in your browser at `http://localhost:3000`.

4.  **Interact:** Type your text into the input box and observe the aura visualization change as you analyze different sentiments.

## Development

This utility is built with React and uses a simple JavaScript module for sentiment analysis. Tests are written with React Testing Library and Jest.

## Project Structure

```
nightly-aura-reader/
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.js
│   ├── AuraDisplay.js
│   ├── index.js
│   └── sentimentAnalyzer.js
└── tests/
    └── App.test.js
```
