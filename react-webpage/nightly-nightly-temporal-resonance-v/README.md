# Nightly Temporal Resonance Visualizer

## Summary
This utility is an interactive React web application designed to visualize and track "temporal event resonances." Users can input events with a name, date, and a 'resonance strength' (1-10). The application then displays these events and calculates an overall 'temporal resonance score' for the current moment, offering a whimsical yet insightful look into the echoes of past and potential future events.

## How to Run
1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-temporal-resonance-viz
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Start the development server:**
    ```bash
    npm run dev
    ```
    This will typically open the application in your browser at `http://localhost:5173` (or a similar port).

4.  **Build for production (optional):**
    ```bash
    npm run build
    ```
    This will create a `dist` folder with the optimized production build.

## How to Use
1.  **Add a Temporal Event:** Use the input form to enter:
    *   **Event Name:** A descriptive name for your temporal event (e.g., "The Great Coffee Spill", "Whispers of the Void").
    *   **Event Date:** The date and time when the event occurred or is predicted to occur.
    *   **Resonance Strength:** A number from 1 to 10 indicating how strongly this event resonates through the temporal fabric (1 being weak, 10 being very strong).
2.  **Observe the Echoes:** The added events will appear in the list. The "Overall Temporal Resonance" display will update, giving you a sense of the current temporal energy.

## Project Structure
```
nightly-temporal-resonance-viz/
├── README.md
├── package.json
├── vite.config.js
├── src/
│   ├── index.html
│   ├── main.jsx
│   ├── App.jsx
│   ├── App.css
│   └── components/
│       ├── EventInput.jsx
│       ├── EventList.jsx
│       └── ResonanceDisplay.jsx
└── tests/
    └── App.test.jsx
```

## Technologies Used
*   **React**: For building the user interface.
*   **Vite**: A fast build tool for modern web projects.
*   **CSS**: For styling.
*   **Vitest / React Testing Library**: For unit testing React components.
