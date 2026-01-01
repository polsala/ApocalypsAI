# Nightly Mood Ring Monitor

## Overview

The `nightly-mood-ring-monitor` is a whimsical-yet-useful React web application designed to provide a quick, visual sentiment analysis of text inputs, such as community logs, daily reports, or any textual data. It displays the 'mood' of the text as a color-changing mood ring, offering a lighthearted way to gauge the collective sentiment.

## Features

*   **Interactive Text Input**: Paste or type any text into the provided textarea.
*   **Real-time Sentiment Analysis**: The mood ring updates instantly as you type.
*   **Whimsical Mood Ring Display**: A colorful ring visually represents the detected sentiment (Positive, Negative, or Neutral).
*   **Simple Keyword-Based Logic**: Uses a deterministic, offline keyword matching algorithm for sentiment detection.
*   **Self-contained React App**: Easy to set up and run locally.

## How to Run

To run this utility, you need Node.js and npm (or yarn) installed on your system.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-mood-ring-monitor
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```

3.  **Start the development server**:
    ```bash
    npm start
    # or yarn start
    ```

    This will open the application in your default web browser, usually at `http://localhost:3000`.

## How to Use

1.  Once the application is running in your browser, you will see a textarea.
2.  Paste or type any text into the textarea. This could be a snippet from a community discussion, a log file, or a personal journal entry.
3.  Observe the mood ring and the 'Current Mood' text below it. They will change color and display the detected sentiment (POSITIVE, NEGATIVE, or NEUTRAL) based on the keywords present in your text.

## Sentiment Logic

The sentiment analysis is performed using a simple, rule-based keyword matching system. It's entirely offline and deterministic.

*   **Positive Keywords**: `['great', 'good', 'happy', 'success', 'thrive', 'hope', 'victory', 'safe', 'calm', 'progress', 'stable', 'secure']`
*   **Negative Keywords**: `['bad', 'sad', 'fail', 'danger', 'threat', 'fear', 'chaos', 'broken', 'lost', 'struggle', 'unstable', 'risk']`

The system counts occurrences of these keywords (case-insensitive). If positive keywords outnumber negative ones, the sentiment is 'positive'. If negative keywords outnumber positive ones, it's 'negative'. If the counts are equal or no keywords are found, the sentiment is 'neutral'.

## Development

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

### Available Scripts

In the project directory, you can run:

*   `npm start`: Runs the app in the development mode.
*   `npm test`: Launches the test runner in the interactive watch mode.
*   `npm run build`: Builds the app for production to the `build` folder.
