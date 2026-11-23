# Nightly Community Aura Ring

## Overview

The `nightly-community-aura-ring` is a whimsical-yet-insightful React web application that visualizes the collective 'aura' or sentiment of recent community activity within the ApocalypsAI repository. It's designed to give a quick, at-a-glance understanding of the prevailing mood – whether things are calm, buzzing with activity, a bit tense, or filled with joy.

While a real-world implementation would connect to GitHub APIs to fetch and analyze actual event data (issues, PRs, comments), this standalone utility uses mocked data and a simplified sentiment analysis logic to demonstrate its concept and functionality.

## Features

*   **Interactive Aura Ring:** A visually distinct ring changes color and displays a mood label based on analyzed sentiment.
*   **Mock Sentiment Analysis:** A simple, keyword-based sentiment analyzer processes mock event data.
*   **Self-Contained:** All necessary React components and logic are included.

## How It Works (Mocked)

1.  **Mock Data:** The application simulates recent GitHub events (e.g., issue comments, PR descriptions) as an array of text messages.
2.  **Sentiment Analysis:** A `SentimentAnalyzer` module processes these messages, looking for keywords to determine a collective mood (e.g., 'Calm', 'Active', 'Tense', 'Joyful', 'Neutral').
3.  **Visualization:** The `MoodRing` component renders a circular visualization, updating its color and text to reflect the detected mood.

## Installation & Usage

To run this utility, you'll need Node.js and npm (or yarn) installed.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-community-aura-ring
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

## Running Tests

To run the automated tests for this utility:

```bash
cd react-webpage/nightly-community-aura-ring
npm test
# or yarn test
```

## Project Structure

```
nightly-community-aura-ring/
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.css
│   ├── App.js
│   ├── index.js
│   ├── MoodRing.css
│   ├── MoodRing.js
│   └── SentimentAnalyzer.js
└── tests/
    ├── App.test.js
    └── SentimentAnalyzer.test.js
```
