# Nightly Wasteland Aura Reader

A whimsical React web utility to discern the 'aura' or underlying emotional and thematic tone of text snippets from the post-apocalyptic wasteland. Ever wondered if that cryptic message from a fellow wanderer carries 'Scavenger's Hope' or 'Despair-ridden Gloom'? This tool will help you find out!

## Features

*   **Text Input**: Paste or type any text into the designated area.
*   **Aura Analysis**: Categorizes text into one of several whimsical aura types based on keyword detection.
*   **Visual Feedback**: Displays the detected aura with a corresponding color and descriptive text.

## Aura Types

*   **Despair-ridden Gloom**: Signifies negative, hopeless, or dangerous sentiments.
*   **Scavenger's Hope**: Indicates resourceful, optimistic, or survival-oriented themes.
*   **Temporal Ripple**: Points to time-related, anomaly-suggesting, or distorted elements.
*   **Whispers of the Void**: Suggests mysterious, existential, or unknown forces at play.
*   **Neutral Dust**: For common, unclassified, or mundane text with no strong aura.

## How to Run

1.  **Prerequisites**: Ensure you have Node.js (v14 or higher) and npm (or yarn) installed on your system.
2.  **Navigate**: Change your current directory to `nightly-wasteland-aura-reader`.
3.  **Install Dependencies**:
    ```bash
    npm install
    # or yarn install
    ```
4.  **Start the Development Server**:
    ```bash
    npm start
    # or yarn start
    ```
    This command will compile the React application and open it in your default web browser, typically at `http://localhost:3000`.

## How to Use

1.  Once the application is running in your web browser, locate the large text area.
2.  Type or paste any text you wish to analyze (e.g., a diary entry, a radio transmission, a cryptic note).
3.  Click the "Read Aura" button below the text area.
4.  The detected aura type and its associated color will be displayed prominently below the button.

## Project Structure

```
nightly-wasteland-aura-reader/
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.js
│   ├── App.css
│   ├── AuraAnalyzer.js
│   ├── AuraDisplay.js
│   └── index.js
└── tests/
    └── AuraAnalyzer.test.js
```
