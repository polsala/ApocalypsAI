# Nightly Temporal Echo Visualizer

An interactive web interface designed to help survivors understand and visualize temporal echoes and ripples, providing insights into chronological distortions.

## Features

*   **Temporal Anchor Input**: Specify a point in time or a significant event.
*   **Echo Generation**: Simulate and display 'Past Whispers', 'Future Ripples', and a 'Distortion Index' based on the anchor.
*   **Interactive Display**: Visually distinct cards for different types of temporal echoes.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-temporal-echo-visualizer
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Start the development server**:
    ```bash
    npm run dev
    ```
    This will typically open the application in your browser at `http://localhost:5173` (or a similar port).

4.  **Build for production**:
    ```bash
    npm run build
    ```
    This will create a `dist` directory with the optimized production build.

## How to Use

1.  Open the application in your web browser.
2.  Enter a "Temporal Anchor" into the input field (e.g., "The Great Silence", "Yesterday's Ration Drop", "Year 2042").
3.  Click the "Generate Echoes" button.
4.  Observe the generated temporal echoes, which will appear as cards below the input, each with a type, content, and simulated intensity.

## Development

This utility is built using React with Vite for a fast development experience.

### Testing

To run the automated tests:

```bash
npm test
```

Tests are written using Vitest and `@testing-library/react` to ensure component functionality and deterministic echo generation.
