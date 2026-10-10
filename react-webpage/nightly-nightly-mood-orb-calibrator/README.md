# Nightly Mood Orb Calibrator

## Overview

The Nightly Mood Orb Calibrator is a whimsical-yet-useful React web application designed to help the community quickly gauge the emotional resonance of text inputs. In the post-apocalyptic landscape, understanding the underlying sentiment of messages, log entries, or communications can be crucial for maintaining morale and making informed decisions. Simply paste any text, and the Mood Orb will visually represent its dominant sentiment (positive, neutral, or negative) through color and emoji.

## Features

*   **Text Input**: A simple textarea to paste any message.
*   **Sentiment Analysis**: Basic client-side keyword-based sentiment detection.
*   **Visual Feedback**: An interactive "Mood Orb" that changes color and displays an emoji based on the detected sentiment.

## Installation & Usage

To run this utility, you'll need Node.js and npm (or yarn) installed.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-mood-orb-calibrator
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```

3.  **Start the development server**:
    ```bash
    npm start
    # or yarn start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

4.  **Use the application**: Type or paste text into the provided textarea and click "Calibrate Mood" to see the Mood Orb react.

## Running Tests

To run the automated tests:

```bash
cd react-webpage/nightly-mood-orb-calibrator
npm test
# or yarn test
```

## Project Structure

```
nightly-mood-orb-calibrator/
├── README.md
├── package.json
├── src/
│   ├── index.js          # Entry point for the React app
│   ├── App.js            # Main application component
│   ├── MoodOrb.js        # Visual component for the sentiment display
│   ├── SentimentAnalyzer.js # Utility for basic text sentiment analysis
│   └── App.css           # Basic styling
└── tests/
    ├── App.test.js
    ├── MoodOrb.test.js
    └── SentimentAnalyzer.test.js
```
