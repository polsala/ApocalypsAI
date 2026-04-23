# Nightly AI Mood Monitor

## Summary

This utility provides a whimsical, interactive web interface to visualize the collective 'mood' of the ApocalypsAI agents. While the mood is simulated for this standalone utility, in a grander scheme, it could reflect sentiment analysis of agent logs, commit messages, or workflow statuses. It offers a quick, color-coded glance at the 'emotional state' of our automated collective.

## Features

*   **Dynamic Mood Display**: A 'mood ring' that changes color and description.
*   **Simulated Activity**: A button to refresh the mood, simulating new agent activity.
*   **Whimsical Descriptions**: Fun, apocalypse-themed mood interpretations.

## How to Run

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-ai-mood-monitor
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

## How to Develop

*   The main application logic resides in `src/App.js` and `src/MoodRing.js`.
*   Mood generation logic is in `src/utils.js`.
*   Styling is in `src/MoodRing.css`.

## How to Test

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-ai-mood-monitor
    ```
2.  **Run tests:**
    ```bash
    npm test
    ```
    This will execute the tests defined in `tests/MoodRing.test.js`.

## Project Structure

```
nightly-ai-mood-monitor/
├── public/
│   └── index.html
├── src/
│   ├── App.js
│   ├── index.js
│   ├── index.css
│   ├── MoodRing.css
│   ├── MoodRing.js
│   └── utils.js
├── tests/
│   └── MoodRing.test.js
├── package.json
└── README.md
```
