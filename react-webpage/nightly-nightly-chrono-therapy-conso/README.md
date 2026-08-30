# Nightly Chrono-Therapy Console

## Overview

The `nightly-chrono-therapy-console` is a whimsical-yet-useful interactive web application designed to help the community navigate the emotional and psychological impacts of temporal anomalies. In a world where time itself can be... flexible, this console provides a structured way to log temporal distortions, track personal mood fluctuations, and engage in reflective prompts to maintain mental equilibrium.

It's a personal sanctuary for your sanity, built with React, offering a simple, self-contained interface that stores your temporal logs and mood data directly in your browser's local storage.

## Features

*   **Temporal Distortion Log**: Record any unusual temporal events, paradoxes, or chronological ripples you encounter.
*   **Chronological Ripple Intensity (Mood Tracker)**: A simple slider to rate your current emotional state or stress level, helping you visualize your well-being over time.
*   **Mood Fluctuation Chart**: A basic list-based visualization of your logged moods, showing trends and patterns.
*   **Reflection Prompts**: Daily (or whenever you visit) prompts to encourage introspection on your temporal experiences.
*   **Local Storage Persistence**: All your logs and mood entries are saved directly in your browser, ensuring your data is private and persists across sessions.

## How to Run

This utility is a standard React application built with Vite. To get it up and running:

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-chrono-therapy-console
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Start the development server**:
    ```bash
    npm run dev
    ```
    This will typically open the application in your browser at `http://localhost:5173` (or another available port).

4.  **Build for production (optional)**:
    ```bash
    npm run build
    ```
    This will create a `dist` folder with optimized static assets, ready for deployment.

## How to Use

Once the application is running:

1.  **Log Temporal Distortion**: Use the text area under "Log Temporal Distortion" to describe any time-related oddities. Click "Log Event" to save it.
2.  **Track Mood**: Adjust the slider under "Chronological Ripple Intensity (Mood Tracker)" to reflect your current mood (1 being very low, 10 being very high). Click "Log Mood" to record it.
3.  **Review Logs**: Your logged events and moods will appear in their respective sections below.
4.  **Reflect**: Consider the daily reflection prompt to gain deeper insight into your temporal journey.

## Development & Testing

*   **Linting**: `npm run lint`
*   **Tests**: `npm run test` (uses Vitest and React Testing Library)

## Project Structure

```
nightly-chrono-therapy-console/
├── public/
├── src/
│   ├── App.jsx           # Main application component, handles state and rendering
│   ├── index.css         # Global styles
│   └── main.jsx          # Entry point for React application
├── tests/
│   ├── App.test.jsx      # Tests for the main App component
│   └── setup.js          # Vitest setup for mocks (e.g., localStorage)
├── .eslintrc.cjs
├── index.html
├── package.json          # Project dependencies and scripts
├── vite.config.js        # Vite configuration
└── README.md
```
