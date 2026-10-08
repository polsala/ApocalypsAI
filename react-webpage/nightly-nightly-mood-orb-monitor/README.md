# Nightly Mood Orb Monitor

## Summary
The Nightly Mood Orb Monitor is a whimsical-yet-useful React web application designed to visualize the collective emotional resonance of the ApocalypsAI community. Users can log their daily sentiment, which then manifests as an animated "Mood Orb" on the dashboard. This provides a quick, intuitive glance at the community's overall well-being.

## How it Works
Each time a community member (or an agent reporting its internal state) logs a sentiment score (from 1 to 10), a new Mood Orb appears. The orb's color, size, and subtle animation reflect the logged sentiment:
- **1-3 (Dim/Flickering)**: Indicates low morale, perhaps "Anxious Echoes" or "Void Whispers".
- **4-7 (Stable/Pulsing)**: Represents neutral or stable sentiment, like "Steady Hum" or "Calm Resonance".
- **8-10 (Gleaming/Vibrant)**: Signifies high spirits, "Radiant Harmony" or "Apocalyptic Joy".

The dashboard also displays a "Collective Resonance" score, an average of the last few logged sentiments, giving a snapshot of the community's current emotional climate.

## Installation and Running
To run this utility, you need Node.js and npm installed.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-mood-orb-monitor
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Start the development server**:
    ```bash
    npm start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

## Usage
1.  Enter a sentiment score (1-10) in the input field.
2.  Click "Log Sentiment" to add your mood as a new Mood Orb.
3.  Observe the orbs change and the "Collective Resonance" update.
4.  Your logged sentiments are stored locally in your browser, persisting across sessions.

## Development
The application is built with React and uses `create-react-app` for its setup.
- `src/App.js`: Main application component, handles state and rendering of orbs.
- `src/MoodOrb.js`: Component for individual mood orbs, responsible for visual representation based on sentiment.
- `src/index.js`: Entry point for React rendering.
- `src/App.css`: Styling for the application.

## Tests
Tests are written using React Testing Library and Jest.
To run tests:
```bash
npm test
```
