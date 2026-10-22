# Nightly Mood Bloom Garden

An interactive React web application that visualizes abstract concepts like community morale, resource abundance, or personal well-being as a dynamic, evolving digital garden. Input your current "mood" or "resource level," and watch the garden bloom, change colors, or reflect the collective state.

## Features

*   **Interactive Mood Input**: Easily adjust a "mood" or "resource" slider.
*   **Dynamic Garden Visualization**: Plants and blooms in the garden react to the input, changing size, color, and animation.
*   **Whimsical & Calming**: A delightful way to observe abstract data.
*   **Self-contained**: Runs entirely in your browser.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-mood-bloom-garden
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

4.  **Build for production (optional)**:
    ```bash
    npm run build
    ```
    This creates a `build` directory with optimized static files.

## Usage

Once the application is running:
1.  Use the slider to set a "Mood Level" (e.g., 1-10).
2.  Observe how the blooms change based on your input! Higher mood levels might result in larger, more vibrant blooms, while lower levels might show smaller, muted ones.

## Project Structure

```
.
├── README.md
├── package.json
├── src/
│   ├── App.js             # Main application component
│   ├── App.css            # Global styles for App component
│   ├── index.js           # React entry point
│   ├── index.css          # Global styles for body
│   └── components/
│       ├── BloomGarden.js # Renders the garden visualization
│       ├── BloomGarden.css# Styles for the garden
│       ├── MoodInput.js   # Handles user mood input
│       └── MoodInput.css  # Styles for mood input
└── tests/
    └── App.test.js        # Tests for the main App component
```
