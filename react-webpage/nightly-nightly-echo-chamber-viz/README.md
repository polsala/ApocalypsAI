# Nightly Echo Chamber Visualizer

## Overview

The `nightly-echo-chamber-viz` is a whimsical-yet-useful React web application designed to help the community identify recurring themes and 'temporal echoes' within event data. Input a series of timestamped messages, and the visualizer will highlight keywords and phrases that resonate across your data, helping you spot trends, anomalies, or just the persistent whispers of the void.

## Features

*   **Event Input**: Easily add new temporal events with a timestamp and a message.
*   **Echo Analysis**: Processes messages to identify frequently occurring words and phrases.
*   **Interactive Visualization**: Displays the 'echoes' with their frequency, allowing for quick insights into data patterns.

## Installation & Running

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/react-webpage/nightly-echo-chamber-viz
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

## Usage

1.  **Add Events**: Use the input form to add events. Each event requires a timestamp (e.g., `2024-07-20T10:00:00Z`) and a message.
2.  **Observe Echoes**: As you add events, the 'Echoes' section will update, showing the most frequent words and their counts. These are your temporal echoes!
3.  **Clear Data**: A button is provided to clear all input data and start fresh.

## Project Structure

```
nightly-echo-chamber-viz/
├── public/
│   └── index.html
├── src/
│   ├── App.css
│   ├── App.js
│   ├── components/
│   │   ├── EchoInput.js
│   │   └── EchoVisualizer.js
│   └── utils/
│       └── analyzer.js
├── tests/
│   └── analyzer.test.js
├── package.json
└── README.md
```

## Contributing

Feel free to expand the visualization capabilities, add more sophisticated natural language processing, or integrate with external data sources. Pull requests are welcome!
