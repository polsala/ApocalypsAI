# Nightly Temporal Echo Visualizer

## Summary

This utility is an interactive React web application designed to visualize the 'temporal echoes' of specified keywords or phrases within a given text dataset. It helps users identify trends, spikes, and decay in the frequency of terms over time, offering a whimsical yet useful way to understand textual dynamics.

## Features

*   **Text Input**: Paste or type your text data directly into the application.
*   **Keyword Tracking**: Define multiple keywords or phrases to monitor.
*   **Temporal Visualization**: See how the frequency of your keywords changes across 'time slices' of the text.
*   **Interactive Chart**: A dynamic line chart displays the 'echoes' with clear indicators of their strength.

## Setup and Running

To run this React application locally:

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-temporal-echo-visualizer
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
    This will open the application in your browser, usually at `http://localhost:3000`.

## Usage

1.  **Input Text**: Paste the text you wish to analyze into the large text area.
2.  **Enter Keywords**: Type the keywords or phrases you want to track, separated by commas (e.g., `anomaly, rift, temporal, echo`).
3.  **Visualize**: The chart will automatically update, showing the frequency of each keyword across the text. Each 'slice' on the X-axis represents a segment of the input text (e.g., every 100 lines).

## Development

This project was bootstrapped with Create React App.

### Available Scripts

In the project directory, you can run:

*   `npm start`: Runs the app in the development mode.
*   `npm test`: Launches the test runner (non-watch mode for CI/CD).
*   `npm run build`: Builds the app for production to the `build` folder.

## Project Structure

```
. 
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── EchoVisualizer.js
│   │   └── InputForm.js
│   ├── utils/
│   │   └── temporalEchoProcessor.js
│   ├── App.css
│   ├── App.js
│   ├── index.css
│   ├── index.js
│   └── reportWebVitals.js
├── tests/
│   ├── temporalEchoProcessor.test.js
│   └── setupTests.js
├── package.json
└── README.md
```
