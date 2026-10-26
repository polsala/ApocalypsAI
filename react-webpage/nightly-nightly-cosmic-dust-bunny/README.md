# Nightly Cosmic Dust Bunny Collector

## Summary

The Nightly Cosmic Dust Bunny Collector is a whimsical React web application designed to make digital decluttering a fun and engaging experience. It visualizes your digital clutter as 'cosmic dust bunnies' floating across your screen. Your mission, should you choose to accept it, is to 'collect' these bunnies by completing actionable, real-world digital cleanup suggestions.

This utility doesn't directly interact with your file system or browser tabs for security and simplicity. Instead, it provides prompts and tracks your progress, turning the mundane task of digital organization into a satisfying game.

## Features

*   **Interactive Dust Bunnies**: Watch cosmic dust bunnies float around. Click them to 'collect' them!
*   **Actionable Suggestions**: Get whimsical yet practical suggestions for cleaning up your digital life.
*   **Progress Tracking**: See how many dust bunnies you've collected and suggestions you've completed.
*   **Whimsical Theme**: Enjoy a lighthearted approach to a common problem.

## How to Run

1.  **Prerequisites**: Ensure you have Node.js (v14+) and npm (or yarn) installed.
2.  **Navigate**: Change into the `nightly-cosmic-dust-bunny` directory:
    ```bash
    cd react-webpage/nightly-cosmic-dust-bunny
    ```
3.  **Install Dependencies**: Install the necessary Node.js packages:
    ```bash
    npm install
    # or yarn install
    ```
4.  **Start the Application**: Launch the React development server:
    ```bash
    npm start
    # or yarn start
    ```
    This will typically open the application in your default web browser at `http://localhost:3000`.

## How to Use

Once the application is running:

1.  **Observe**: Watch the cosmic dust bunnies float around the screen.
2.  **Collect Dust Bunnies**: Click on a dust bunny to 'collect' it. Each collected dust bunny contributes to your score.
3.  **Complete Suggestions**: Review the list of digital decluttering suggestions. When you've performed an action (e.g., closed old tabs, deleted old files), click the 'Complete' button next to the suggestion to mark it as done.
4.  **Enjoy**: Feel the satisfaction of a cleaner digital space, one dust bunny at a time!

## Project Structure

```
nightly-cosmic-dust-bunny/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── DustBunny.js
│   │   └── SuggestionCard.js
│   ├── App.css
│   ├── App.js
│   ├── index.css
│   └── index.js
├── tests/
│   └── App.test.js
├── package.json
└── README.md
```

## Development Notes

This project was bootstrapped with Create React App. For more information on available scripts, refer to the [Create React App documentation](https://create-react-app.dev/docs/getting-started).
