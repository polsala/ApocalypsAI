# Nightly Wasteland Whimsy Weaver

An interactive React web app that generates a whimsical daily forecast for the wasteland, combining environmental factors and a 'mood' score. Perfect for a moment of lightheartedness amidst the desolation.

## Features

*   **Whimsical Forecasts**: Get a unique combination of weather, resource status, and wasteland mood.
*   **Interactive Reroll**: Don't like today's forecast? Reroll for a new one!
*   **Simple UI**: A clean, post-apocalyptic-themed interface.

## How to Run

This utility is a standard Create React App project.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-wasteland-whimsy-weaver
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

## How to Test

To run the automated tests for this utility:

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-wasteland-whimsy-weaver
    ```

2.  **Run the tests**:
    ```bash
    npm test
    ```
    This will execute the tests using `react-scripts test` (Jest and React Testing Library).

## Project Structure

```
.
├── README.md
├── package.json
├── src/
│   ├── App.css
│   ├── App.jsx
│   ├── index.css
│   ├── index.js
│   └── WhimsyGenerator.js
└── tests/
    └── App.test.jsx
```
