# Nightly Mood Ring Monitor

An interactive web interface to visualize the emotional "temperature" of text inputs, helping gauge community sentiment in the post-apocalyptic landscape.

## Overview

In times of uncertainty, understanding the collective mood is crucial. The Nightly Mood Ring Monitor provides a simple, whimsical tool to analyze text – be it community announcements, log entries, or cryptic whispers from the void – and visually represent its underlying sentiment. Just type or paste text, and watch the Mood Ring change color, reflecting the emotional tone.

## Features

*   **Real-time Sentiment Analysis**: Instantly processes text input to determine its emotional score.
*   **Whimsical Mood Ring Visualization**: A color-changing ring visually represents the sentiment:
    *   **Green/Lime**: Positive sentiment
    *   **Orange/Red**: Negative sentiment
    *   **Grey**: Neutral sentiment
*   **Intensity Indication**: Displays whether the mood is mildly, moderately, or strongly positive/negative.
*   **Self-contained Web App**: Easy to deploy and run in any modern browser.

## How to Run

This utility is a standard React application.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-mood-ring-monitor
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Start the development server**:
    ```bash
    npm start
    ```
    This will open the application in your default browser at `http://localhost:3000`.

4.  **Build for production (optional)**:
    ```bash
    npm run build
    ```
    This will create a `build` directory with the optimized production-ready files. You can then serve these static files using any web server.

## How to Use

1.  Open the application in your web browser.
2.  Type or paste any text into the provided textarea.
3.  Observe the Mood Ring:
    *   Its color will change to reflect the sentiment (green for positive, red for negative, grey for neutral).
    *   The accompanying text will indicate the intensity and type of mood (e.g., "Strongly Positive", "Mildly Negative").
    *   A numerical sentiment score is also displayed.

## Automated Tests

To ensure the sentiment analysis and visualization components function as expected, run the automated tests:

```bash
cd react-webpage/nightly-mood-ring-monitor
npm test -- --watchAll=false
```

The tests are deterministic and offline, relying on predefined word lists for sentiment analysis and mocking the React DOM for component rendering.

## Project Structure

```
.
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.css
│   ├── App.js
│   ├── index.css
│   ├── index.js
│   └── components/
│       ├── MoodRing.css
│       ├── MoodRing.js
│       └── SentimentAnalyzer.js
└── tests/
    ├── MoodRing.test.js
    └── SentimentAnalyzer.test.js
```
