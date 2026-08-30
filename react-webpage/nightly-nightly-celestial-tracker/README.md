# Nightly Celestial Alignment Tracker

## Overview

The `nightly-celestial-tracker` is a whimsical-yet-insightful React web application designed for the ApocalypsAI community. In a world of uncertainty, sometimes a little cosmic guidance can go a long way. This tool visualizes the simulated alignment of various celestial bodies and offers a daily 'cosmic influence' report, providing a fun, abstract way to consider daily challenges and opportunities.

While the celestial mechanics are entirely simulated and deterministic (no actual astrophysics involved!), the tracker offers a consistent, repeatable source of 'cosmic wisdom' that can be used for anything from deciding the best day for a scavenging run to simply adding a touch of wonder to your post-apocalyptic routine.

## Features

*   **Interactive Celestial Map**: See the positions of five key celestial bodies: Solara, Lunaris, Terra Nova, Aetheria, and Umbra.
*   **Daily Influence Report**: Get a unique, whimsical 'influence' message based on the day's celestial alignments.
*   **Date Navigation**: Easily jump to different dates to see past alignments or predict future ones.
*   **Deterministic Simulation**: The celestial positions and influences are consistently generated based on the date, ensuring repeatable results.

## Celestial Bodies & Their Whimsical Meanings

*   **Solara**: Represents energy, vitality, and direct action.
*   **Lunaris**: Symbolizes intuition, emotional currents, and hidden depths.
*   **Terra Nova**: Signifies stability, resources, and new beginnings.
*   **Aetheria**: Embodies innovation, communication, and ethereal insights.
*   **Umbra**: Denotes introspection, shadows, and uncovering forgotten truths.

## Installation & Usage

To run this utility, you'll need Node.js and npm installed.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-celestial-tracker
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

4.  **Interact with the tracker:**
    Use the date picker to select a date and observe the celestial alignments and their reported influences.

## Running Tests

To ensure the cosmic calculations are always precise (in their simulated way!), run the automated tests:

```bash
cd react-webpage/nightly-celestial-tracker
npm test
```

## Project Structure

```
nightly-celestial-tracker/
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.js             # Main application component
│   ├── CelestialBody.js   # Component for rendering a single celestial body
│   ├── AlignmentDisplay.js# Component for displaying alignment influences
│   ├── utils.js           # Core logic for celestial position and alignment calculations
│   ├── api.js             # Mock API for fetching celestial data
│   ├── index.js           # React entry point
│   └── index.css          # Basic styling
└── tests/
    ├── App.test.js
    ├── CelestialBody.test.js
    ├── AlignmentDisplay.test.js
    ├── utils.test.js
    └── api.test.js
```
