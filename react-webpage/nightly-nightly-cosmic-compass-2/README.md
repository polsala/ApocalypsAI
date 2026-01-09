# Nightly Cosmic Compass

## Overview

The Nightly Cosmic Compass is a whimsical web utility designed to help you find your 'cosmically optimal' spot for daily activities. Ever wondered if the void whispers are more favorable for your morning coffee in the kitchen or the living room? This compass will give you a fun, entirely arbitrary, yet strangely compelling recommendation!

It provides an interactive map (simulated for simplicity and offline testing) and a 'Cosmic Alignment Score' to guide your decisions, from where to read a book to where to ponder the existential dread of the universe.

## Features

*   **Cosmic Alignment Score**: A numerical value indicating the perceived 'cosmic harmony' of a location.
*   **Optimal Location Suggestion**: A whimsical recommendation for where you should be.
*   **Interactive Map Display**: Visualizes the suggested location (mocked for this utility).
*   **Whimsical Prompts**: Fun messages to accompany your cosmic journey.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-cosmic-compass
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

## How to Use

1.  Open the application in your web browser.
2.  Click the "Scan for Cosmic Alignment" button.
3.  Observe your new Cosmic Alignment Score and the suggested optimal location on the map.
4.  Follow the compass's whimsical guidance, or don't! It's all in good fun.

## Development Notes

*   The map display is a simplified component for demonstration and testing purposes. It does not integrate with external map APIs.
*   Cosmic alignment calculations are entirely client-side and based on a pseudo-random, whimsical algorithm.

## Tests

To run the tests:

```bash
npm test
```

Tests are designed to be deterministic and run offline, mocking any external dependencies or complex UI interactions.
