# Nightly Chrono-Emotional Compass

## Overview

The Nightly Chrono-Emotional Compass is a whimsical-yet-insightful React web application designed to visualize the collective emotional 'vibe' of the ApocalypsAI community over time. It simulates activity logs (like commit messages, issue titles, or PR descriptions) and assigns a 'mood score' to each, presenting a temporal overview of the project's emotional state.

While currently operating on simulated data for demonstration and self-containment, this utility lays the groundwork for future integration with actual repository activity, offering a unique perspective on project health and team morale.

## How it Works

The application displays a series of 'mood events' on a timeline. Each event is represented by a colored bar or segment, where the color indicates the emotional score:

*   **Red (Very Negative):** Scores -10 to -5 (e.g., "Critical failure", "System meltdown")
*   **Orange (Negative):** Scores -4 to -1 (e.g., "Bug fix", "Minor issue")
*   **Yellow (Neutral):** Score 0 (e.g., "Refactor", "Docs update")
*   **Light Green (Positive):** Scores 1 to 4 (e.g., "New feature", "Improvement")
*   **Green (Very Positive):** Scores 5 to 10 (e.g., "Major breakthrough", "Optimized everything")

The data is currently mocked to ensure deterministic behavior and offline testing, but the structure is ready for real-world data integration.

## Installation

To run this utility, you need Node.js and npm (or yarn) installed on your system.

1.  Navigate into the `nightly-chrono-emo-compass` directory:
    ```bash
    cd nightly-chrono-emo-compass
    ```
2.  Install the necessary dependencies:
    ```bash
    npm install
    # or yarn install
    ```

## Usage

To start the development server and view the application in your browser:

```bash
npm start
# or yarn start
```

This will typically open the application at `http://localhost:3000`.

## Tests

To run the automated tests for the application:

```bash
npm test
# or yarn test
```

Tests are written using Jest and React Testing Library and are designed to be deterministic and offline, relying on mocked data.
