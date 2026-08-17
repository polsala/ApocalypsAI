# Nightly Lumina-Loom: A Mood-Driven Color Palette Generator

## Summary
The Nightly Lumina-Loom is a whimsical web utility designed to bring a splash of color and emotional resonance to the post-apocalyptic world. It allows survivors to select a "mood" – from the depths of 'Despair' to the heights of 'Hope' – and instantly generates a corresponding, aesthetically pleasing 5-color palette. Perfect for decorating your salvaged shelter, personalizing your gear, or simply finding a moment of visual beauty amidst the chaos.

## Features
*   **Mood-Driven Palettes**: Select from a range of post-apocalyptic moods.
*   **Instant Generation**: Get a unique 5-color palette with hex codes.
*   **Whimsical Interface**: A simple, intuitive web interface built with React.

## How to Run
This utility is a standard React application. To run it, you'll need Node.js and npm installed.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-lumina-loom
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Start the development server**:
    ```bash
    npm start
    ```
    This will open the application in your default web browser, usually at `http://localhost:3000`.

## How to Use
1.  Open the application in your web browser.
2.  Select a mood from the dropdown menu (e.g., "Hope", "Despair", "Scrappy").
3.  Observe the generated color palette displayed below. Each color swatch shows its hexadecimal code.

## Development Notes
This utility is built using React.js. The color generation logic is deterministic for each mood, ensuring consistent yet varied palettes based on HSL color manipulation.

## Tests
To run the automated tests:
```bash
cd react-webpage/nightly-lumina-loom
npm test
```
