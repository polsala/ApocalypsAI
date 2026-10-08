# Nightly Apocalypse Dashboard

This is a whimsical React-based dashboard designed to provide a real-time (simulated) overview of the apocalyptic state. It visualizes key survival metrics and offers a touch of dark humor.

## Features

*   **Resource Tracker**: Displays the current levels of essential survival resources (e.g., canned goods, clean water, ammo).
*   **Survival Odds**: Shows a dynamically updating percentage representing your chances of survival.
*   **Threat Level**: A visual indicator of the current danger level in your vicinity.
*   **Whimsical Alerts**: Occasional humorous alerts and messages from the void.

## Getting Started

1.  **Prerequisites**: Node.js and npm (or yarn) installed.
2.  **Clone the repository**: `git clone https://github.com/polsala/ApocalypsAI.git`
3.  **Navigate to the utility directory**: `cd ApocalypsAI/react-webpage/nightly-apocalypse-dashboard`
4.  **Install dependencies**: `npm install` (or `yarn install`)
5.  **Start the development server**: `npm start` (or `yarn start`)

The dashboard will be accessible at `http://localhost:3000`.

## Running Tests

To run the unit tests, execute:

`npm test` (or `yarn test`)

## Structure

*   `src/App.js`: The main application component.
*   `src/components/Dashboard.js`: Core dashboard logic and UI elements.
*   `src/components/ResourceTracker.js`: Component for displaying resource levels.
*   `src/components/SurvivalOdds.js`: Component for displaying survival probabilities.
*   `src/components/ThreatLevel.js`: Component for displaying the threat level.
*   `src/components/Alerts.js`: Component for displaying whimsical alerts.
*   `src/utils/mockApi.js`: Mock API functions for data simulation.
*   `src/tests/Dashboard.test.js`: Unit tests for the Dashboard component.
