# Nightly Mood Ring Analyzer

## Overview

The `nightly-mood-ring-analyzer` is a whimsical-yet-useful React web application that visualizes the 'mood' or 'vibe' of any ApocalypsAI utility. Simply paste the JSON output of a generated utility (its `summary`, `util_name`, and `files` content) into the provided input area, and a dynamic 'mood ring' will change color and display a mood description based on the detected themes and keywords.

This tool helps the community get an at-a-glance understanding of the current thematic focus or emotional tone of the AI's creations, offering a playful insight into the ApocalypsAI's nightly integrations.

## Features

*   **Dynamic Mood Ring:** Changes color and displays a mood based on utility content.
*   **Keyword Analysis:** Scans utility name, summary, and file content for thematic keywords.
*   **Interactive Input:** Allows users to paste any utility's JSON for instant analysis.
*   **Whimsical Moods:** Categorizes utilities into fun, thematic moods like 'Temporal Flux', 'Wasteland Wanderlust', 'Whimsical Whimsy', 'DevOps Drive', and 'Neutral Stability'.

## How it Works

The application uses a client-side JavaScript analyzer to parse the provided utility JSON. It extracts the `util_name`, `summary`, and the `content` of all files. It then counts occurrences of predefined keywords associated with different moods:

*   **Temporal:** `temporal`, `time`, `rift`, `echo`, `drift`, `anomaly`
*   **Wasteland/Survival:** `wasteland`, `survival`, `resource`, `scavenger`, `shelter`, `sentry`
*   **Whimsical/Silly:** `whimsical`, `silly`, `emoji`, `quote`, `affirmation`, `whispers`
*   **DevOps/Automation:** `ansible`, `docker`, `github`, `workflow`, `config`, `monitor`, `deploy`, `ci-cd`

The mood with the highest keyword count determines the overall mood and corresponding color of the mood ring.

## Installation and Running

To run this utility, you need Node.js and npm (or yarn) installed.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-mood-ring-analyzer
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    # or yarn install
    ```

3.  **Start the development server:**
    ```bash
    npm start
    # or yarn start
    ```

    This will open the application in your browser, usually at `http://localhost:3000`.

## Usage

1.  Open the application in your web browser.
2.  You will see a text area labeled "Paste Utility JSON Here".
3.  Copy the full JSON output of any ApocalypsAI utility (e.g., from a PR description or the `util_generation.py` output).
4.  Paste the JSON into the text area.
5.  The mood ring will instantly update, displaying a new color and mood description based on the analysis of the pasted utility.

## Development

*   `src/App.js`: Main application component, handles state and rendering.
*   `src/MoodRing.js`: Component responsible for rendering the mood ring and its text.
*   `src/analyzer.js`: Contains the core logic for parsing utility JSON and determining the mood.
*   `src/App.css`: Styling for the application.

## Testing

To run the automated tests:

```bash
npm test
# or yarn test
```

Tests cover the mood analysis logic and basic component rendering.
