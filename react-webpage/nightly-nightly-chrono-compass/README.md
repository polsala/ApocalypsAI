# Nightly Chrono-Compass

## Overview

The Nightly Chrono-Compass is a whimsical-yet-useful interactive React web application designed to help you map your personal temporal landscape. Ever wonder when your 'Temporal Drift Index' is highest, or when you hit a 'Productivity Nebula'? This tool allows you to log your perceived energy, focus, and subjective time speed throughout the day and visualizes these patterns, helping you understand your personal chronotype and optimize your daily rhythm.

## Features

*   **Intuitive Input:** Easily log your current state with simple sliders for Energy, Focus, and Perceived Time Speed.
*   **Temporal Visualization:** See your daily patterns emerge on a dynamic chart, highlighting your peak and trough periods.
*   **Local Persistence:** Your data is saved locally in your browser, so your insights are always available.
*   **Whimsical Metrics:** Track your 'Temporal Drift Index' (how fast or slow time feels), 'Productivity Nebula' (high focus/energy), and 'Procrastination Black Hole' (low focus/energy).

## How to Use

1.  **Navigate to the App:** Open `index.html` in your web browser, or serve the React app locally.
2.  **Log Your State:** At various points throughout your day, use the sliders to input your current Energy, Focus, and how fast or slow time feels to you (Perceived Time Speed).
3.  **Observe Patterns:** The chart will update in real-time, showing your logged entries. Over time, you'll start to see patterns in your personal temporal perception.
4.  **Gain Insights:** Use these insights to schedule tasks during your peak 'Productivity Nebula' or identify times when you might be prone to a 'Procrastination Black Hole'.

## Development Setup

To run this application locally:

1.  **Install Node.js and npm:** If you don't have them, download from [nodejs.org](https://nodejs.org/).
2.  **Navigate to the `nightly-chrono-compass` directory:**
    ```bash
    cd nightly-chrono-compass
    ```
3.  **Install dependencies:**
    ```bash
    npm install
    ```
4.  **Start the development server:**
    ```bash
    npm start
    ```
    This will typically open the app in your browser at `http://localhost:3000`.

## Project Structure

```
nightly-chrono-compass/
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.css
│   ├── App.js
│   ├── ChronoChart.js
│   ├── ChronoInput.js
│   └── index.js
└── tests/
    └── App.test.js
```

## Technologies Used

*   React
*   JavaScript (ES6+)
*   CSS
*   Chart.js (for visualization)
*   Jest & React Testing Library (for testing)
