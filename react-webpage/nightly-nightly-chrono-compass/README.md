# Nightly Chrono-Compass

## Overview

The Nightly Chrono-Compass is a whimsical-yet-useful React web application designed to help you visualize your daily "temporal energy" distribution. Input your tasks or events, assign an estimated time duration, and give them an emotional "charge" (positive, neutral, or negative). The Chrono-Compass will then render an interactive radial chart, showing you where your time and emotional energy are being spent.

This tool is perfect for self-reflection, identifying productivity patterns, and understanding the emotional impact of your daily activities in the post-apocalyptic landscape.

## Features

*   **Task Input**: Easily add new tasks with names, durations (in minutes), and emotional charges.
*   **Temporal Visualization**: See your day's activities represented as a radial chart, where each segment's size reflects its duration and its color indicates its emotional charge.
*   **Emotional Insight**: Quickly identify which activities contribute positively or negatively to your overall temporal energy.
*   **Simple & Intuitive**: A clean, user-friendly interface for quick data entry and visualization.

## How to Run

To get the Nightly Chrono-Compass up and running, follow these steps:

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-chrono-compass
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Start the development server**:
    ```bash
    npm start
    ```
    This will open the application in your default web browser, usually at `http://localhost:3000`.

## How to Use

1.  **Add a Task**: Use the input form at the top of the page.
    *   **Task Name**: A brief description of your activity (e.g., "Scavenge for parts", "Repair water purifier", "Meditate on the void").
    *   **Duration (minutes)**: The estimated time you spent or will spend on the task.
    *   **Emotional Charge**: Select "Positive", "Neutral", or "Negative" to reflect how the task makes you feel.
2.  **Submit**: Click the "Add Task" button. The task will appear in the list and be added to the Chrono-Compass visualization.
3.  **Observe**: The radial chart will dynamically update, showing you the distribution of your temporal energy. Positive tasks are green, neutral are grey, and negative are red.

## Project Structure

```
nightly-chrono-compass/
├── public/
│   └── index.html          # Main HTML file
├── src/
│   ├── App.css             # Global styles
│   ├── App.js              # Main application component
│   ├── ChronoCompass.js    # Radial chart visualization component
│   ├── index.css           # Base styles
│   ├── index.js            # React app entry point
│   └── TaskInput.js        # Component for adding tasks
├── package.json            # Project dependencies and scripts
├── package-lock.json
└── tests/
    ├── App.test.js         # Tests for the App component
    └── ChronoCompass.test.js # Tests for the ChronoCompass component
```
