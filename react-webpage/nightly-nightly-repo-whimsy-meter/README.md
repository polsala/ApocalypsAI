# Nightly Repository Whimsy-Meter

## Overview

The `nightly-repo-whimsy-meter` is a whimsical-yet-useful React web application designed to provide a quick, at-a-glance overview of the ApocalypsAI repository's current 'mood' and activity. It features a 'Whimsy Score' that attempts to quantify the creative and playful spirit of recent contributions, alongside practical metrics like new utilities, open pull requests, and active issues.

## Features

*   **Whimsy Score Visualization**: A 'Chaos Crystal' that changes color and intensity based on the calculated Whimsy Score.
*   **Activity Panel**: Displays key repository metrics such as:
    *   Number of new utilities integrated.
    *   Count of open Pull Requests.
    *   Number of active issues.
*   **Interactive Interface**: A simple, single-page application built with React.

## Whimsy Score Calculation (Mock Logic)

In a real-world scenario, the Whimsy Score would be derived from analyzing commit messages, utility names, issue titles, and agent responses for keywords, emoji usage, and general sentiment. For this standalone utility, the score is simulated based on a mock API response, representing a hypothetical backend analysis.

## Setup and Running

This utility is a standard Create React App project. To run it locally:

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-repo-whimsy-meter
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

## Project Structure

```
nightly-repo-whimsy-meter/
├── public/
│   └── index.html          # Main HTML file
├── src/
│   ├── App.css             # Styling for the main App component
│   ├── App.js              # Main React component, fetches data and orchestrates others
│   ├── App.test.js         # Tests for the App component
│   ├── ActivityPanel.js    # Component to display repository activity stats
│   ├── WhimsyMeter.js      # Component to visualize the 'Whimsy Score'
│   └── index.js            # React application entry point
├── package.json            # Project dependencies and scripts
└── README.md               # This file
```

## Technologies Used

*   React
*   JavaScript (ES6+)
*   CSS
*   Create React App (for project scaffolding and build tooling)
*   Jest & React Testing Library (for testing)
