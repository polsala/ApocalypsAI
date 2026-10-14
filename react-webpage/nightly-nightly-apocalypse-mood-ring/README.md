# Nightly Apocalypse Mood Ring

An interactive React web interface designed to visualize the simulated collective emotional state of the ApocalypsAI community. It offers whimsical insights and coping mechanisms, helping agents and users gauge the 'vibe' of the digital wasteland.

## Features

*   **Dynamic Mood Display**: Shows a current "mood" (e.g., "Chaotic", "Serene", "Optimistic") with a corresponding color and icon.
*   **Whimsical Insights**: Provides a short, context-sensitive message or action item based on the current mood.
*   **Simulated Mood Swings**: Allows users to trigger a new random mood, simulating the unpredictable nature of the apocalypse.
*   **Self-Contained**: Runs entirely client-side, no backend required.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-apocalypse-mood-ring
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    # or
    yarn install
    ```
3.  **Start the development server**:
    ```bash
    npm start
    # or
    yarn start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

## How to Use

Click the "Simulate New Mood" button to cycle through different simulated moods. Observe the color changes, icons, and the accompanying whimsical insights.

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
│   ├── index.js
│   └── moodData.js
└── tests/
    └── App.test.js
```

## Technologies Used

*   React
*   CSS
*   JavaScript
*   Jest & React Testing Library (for tests)
