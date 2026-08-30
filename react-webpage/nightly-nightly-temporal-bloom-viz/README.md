# Nightly Temporal Bloom Visualizer

A React web application that visualizes abstract "temporal bloom" patterns based on user-defined parameters, offering a calming, interactive display.

## Purpose

In the chaotic aftermath, understanding the subtle energies of temporal distortions can be... overwhelming. The Nightly Temporal Bloom Visualizer provides a whimsical, yet conceptually insightful, interface to observe these energies. Adjust parameters like "Resonance Frequency," "Bloom Intensity," and "Decay Rate" to see how the temporal fabric might visually manifest its echoes and ripples. It's perfect for a moment of calm reflection or as a dynamic background for your command console.

## How to Run

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-temporal-bloom-viz
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

## How to Interact

The application presents a canvas displaying the temporal bloom and a set of sliders.
*   **Resonance Frequency:** Adjusts the speed and complexity of the pattern's evolution.
*   **Bloom Intensity:** Controls the vibrancy and density of the visual elements.
*   **Decay Rate:** Determines how quickly old patterns fade, influencing the trail and persistence.

Experiment with these controls to discover unique and mesmerizing temporal manifestations!

## Project Structure

```
.
├── README.md
├── package.json
├── src/
│   ├── App.css
│   ├── App.js
│   ├── index.js
│   ├── setupTests.js
│   └── components/
│       └── TemporalBloomCanvas.js
└── tests/
    └── TemporalBloomCanvas.test.js
```
