# Nightly Morale Meter

## Overview

The `nightly-morale-meter` is a whimsical-yet-useful React web application designed to help the community track and visualize their collective morale. In the face of the apocalypse, keeping spirits up is crucial! This tool allows individuals to log their current morale level and receive instant, context-aware, and often humorous feedback. Over time, it builds a history of morale entries, offering a glimpse into the emotional landscape of the survivors.

## Features

*   **Interactive Morale Input**: Easily select your current morale level using a slider.
*   **Whimsical Feedback**: Receive unique, apocalypse-themed messages based on your morale input.
*   **Morale History**: View a log of past morale entries with their corresponding feedback and timestamps.
*   **Simple & Intuitive UI**: A clean, single-page interface for quick morale logging.
*   **Persistent Storage**: Morale entries are saved locally in your browser, so your history persists across sessions.

## Installation & Setup

To run this utility, you need Node.js and npm (or yarn) installed on your system.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-morale-meter
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
    This will typically open the application in your browser at `http://localhost:3000`.

## Usage

1.  **Adjust the Morale Slider**: Move the slider to reflect your current morale level (1 being lowest, 10 being highest).
2.  **Log Morale**: Click the "Log Morale" button.
3.  **View Feedback**: An instant whimsical message will appear, and your entry will be added to the "Morale History" list.

Keep logging your morale daily to track your emotional journey through the wasteland!

## Development

### Running Tests

To run the automated tests for this utility:

```bash
npm test
# or yarn test
```

### Building for Production

To create a production-ready build of the application:

```bash
npm run build
# or yarn build
```
    This will compile the React app into static files in the `build/` directory, ready for deployment.
