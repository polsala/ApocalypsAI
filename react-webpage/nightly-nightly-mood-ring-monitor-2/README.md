# Nightly Mood Ring Monitor

## Overview

The `nightly-mood-ring-monitor` is a whimsical yet useful React web application designed to help the community quickly visualize and reflect on their emotional state. Users type how they are feeling into an input field, and the digital mood ring dynamically changes color based on detected keywords. Alongside the color change, a tailored affirmation or reflective prompt is displayed, offering a moment of self-care or guidance.

This utility provides a lighthearted way to engage with one's emotions, promoting mindfulness and self-awareness in the often chaotic post-apocalyptic landscape.

## Features

*   **Dynamic Mood Ring:** The central visual element, a circular 'mood ring', changes color in real-time based on the user's input.
*   **Keyword-Based Mood Detection:** Simple natural language processing (via keyword matching) to interpret user input and assign a mood (e.g., happy, anxious, calm, sad).
*   **Tailored Affirmations:** Each detected mood triggers a unique, supportive affirmation or reflective message.
*   **Intuitive Interface:** A clean and simple web interface makes it easy for anyone to use.
*   **Self-Contained:** Runs entirely in the browser after a simple setup, requiring no backend services.

## How to Run

To run the Nightly Mood Ring Monitor locally, follow these steps:

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-mood-ring-monitor
    ```

2.  **Install dependencies:**
    Ensure you have Node.js and npm (or yarn) installed. Then, install the project dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```

3.  **Start the development server:**
    ```bash
    npm start
    # or
    yarn start
    ```
    This will open the application in your default web browser, usually at `http://localhost:3000`.

4.  **Build for production (optional):**
    To create a production-ready build, run:
    ```bash
    npm run build
    # or
    yarn build
    ```
    The optimized static files will be generated in the `build/` directory.

## How to Use

1.  Open the application in your web browser.
2.  Locate the input field labeled "How are you feeling today?".
3.  Type a sentence or a few words describing your current emotional state (e.g., "I feel happy and energetic!", "A bit anxious today.", "Just feeling calm.").
4.  Observe the mood ring change color and a new affirmation appear below the input field, reflecting the detected mood.
5.  Experiment with different words to see how the ring responds!

## Technologies Used

*   **React:** For building the user interface.
*   **JavaScript (ES6+):** The primary language for application logic.
*   **HTML5 & CSS3:** For structuring and styling the web page.
*   **Node.js & npm:** For package management and running the development server.
