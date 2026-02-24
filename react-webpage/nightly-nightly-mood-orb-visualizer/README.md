# nightly-mood-orb-visualizer

An interactive React web application that visualizes the collective "mood" of the ApocalypsAI community as a dynamic, glowing orb. This utility provides a whimsical, at-a-glance representation of simulated sentiment data, offering a unique perspective on the community's emotional state.

## Features

*   **Dynamic Mood Orb**: A visually engaging orb that changes color and animation based on the current "mood" (simulated sentiment).
*   **Simulated Sentiment Stream**: Continuously updates with new, randomized mood data to demonstrate reactivity.
*   **Whimsical Interface**: A lighthearted approach to monitoring community well-being in the post-apocalyptic landscape.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-mood-orb-visualizer
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

## How it Works

The `MoodOrbVisualizer` fetches simulated sentiment data (ranging from -100 to 100) from a local service. This data is then mapped to a color spectrum (e.g., red for low mood, green for high mood) and controls the animation properties of a CSS-animated orb. The simulation updates every few seconds, providing a continuous, evolving display of the community's "pulse."

## Project Structure

```
.
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.css
│   ├── App.js
│   ├── index.css
│   ├── index.js
│   ├── MoodDataService.js
│   └── MoodOrb.js
└── tests/
    ├── App.test.js
    └── MoodOrb.test.js
```

## Automated Tests

To run the tests:

```bash
npm test
```

Tests are written using `@testing-library/react` and Jest, ensuring components render correctly and react to prop changes as expected.
