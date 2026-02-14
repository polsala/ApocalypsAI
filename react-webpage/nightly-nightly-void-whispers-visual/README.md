# Nightly Void Whispers Visualizer

An interactive React web application that allows the community to peer into the 'Void' and visualize its simulated sentiment towards any given text. Ever wondered if your message resonates with hope, despair, whimsy, or dread in the cosmic ether? This tool provides a whimsical, non-scientific interpretation!

## Features

*   **Text Input**: Enter any message, phrase, or thought.
*   **Void Sentiment Analysis (Simulated)**: Our proprietary (and entirely fictional) algorithm processes your text to determine its 'Void Sentiment'.
*   **Multi-Dimensional Visualization**: See the sentiment broken down into categories like Hope, Despair, Whimsy, and Dread, displayed as interactive bars.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-void-whispers-visualizer
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

1.  Type your message into the text area.
2.  Click the "Analyze Whispers" button.
3.  Observe the sentiment bars adjust, revealing the Void's (simulated) feelings!

## Development & Testing

To run the tests:
```bash
npm test
```

## Project Structure

```
.
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   ├── index.css
│   ├── components/
│   │   └── SentimentDisplay.js
│   │   └── SentimentDisplay.css
│   └── utils/
│       └── voidSentiment.js
└── tests/
    └── App.test.js
```
