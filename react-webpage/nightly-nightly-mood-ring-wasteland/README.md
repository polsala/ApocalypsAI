# Nightly Wasteland Mood Ring

The Nightly Wasteland Mood Ring is a whimsical-yet-useful interactive web utility designed to help survivors gauge the emotional tone of their communications, journal entries, or any textual input. In the desolate expanse of the post-apocalyptic world, understanding subtle emotional cues can be crucial. This tool takes your text, performs a rudimentary sentiment analysis, and displays a corresponding "mood ring" color, offering a quick visual summary of the underlying sentiment.

## Features

*   **Text Input**: Enter any message, log, or thought.
*   **Sentiment Analysis**: A simplified, keyword-based analysis determines the emotional tone (positive, neutral, negative, or a mix).
*   **Visual Feedback**: A dynamic "mood ring" changes color to reflect the detected sentiment.
*   **Whimsical Interpretations**: Each color comes with a thematic wasteland interpretation.

## How to Run

1.  **Prerequisites**: Ensure you have Node.js (v14+) and npm (or yarn) installed.
2.  **Navigate**: Change directory into `react-webpage/nightly-mood-ring-wasteland`.
3.  **Install Dependencies**: 
    ```bash
    npm install
    # or yarn install
    ```
4.  **Start the Development Server**: 
    ```bash
    npm start
    # or yarn start
    ```
    This will typically open the application in your browser at `http://localhost:3000`.

## How to Use

1.  Open the application in your web browser.
2.  Type or paste your text into the provided input area.
3.  Observe the "Wasteland Mood Ring" change color and display its interpretation based on the sentiment of your text.

## Example Moods & Colors

*   **Radiant Green (Hopeful)**: "Found a stash of purified water today! Feeling optimistic."
*   **Dusty Grey (Neutral/Observational)**: "The sun rose in the east, as it always does. Another day."
*   **Scorched Red (Distressed/Angry)**: "Those raiders took everything! I swear vengeance!"
*   **Murky Blue (Melancholy/Despair)**: "The silence of the ruins weighs heavy on my soul."
*   **Flickering Amber (Cautious/Uncertain)**: "Heard whispers of a new settlement, but it could be a trap."

## Development Notes

The sentiment analysis is a basic, keyword-driven implementation for demonstration purposes. For a real-world scenario, a more robust NLP model or external API would be required. This utility is designed for self-contained, offline operation.
