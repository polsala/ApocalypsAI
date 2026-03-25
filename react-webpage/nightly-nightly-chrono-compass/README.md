# Nightly Chrono-Compass

## Summary

In the ever-shifting landscape of the post-apocalyptic world, time itself can feel... fluid. The `nightly-chrono-compass` is a whimsical-yet-useful interactive React web application designed to help the community visualize and playfully track perceived temporal shifts and event echoes. Input your significant events, and watch as the Chrono-Compass reveals their 'shifted' present and 'echoed' past, offering a unique perspective on your personal timeline.

## Concept

This utility doesn't actually manipulate time (yet!). Instead, it applies a set of deterministic, pseudo-random temporal offsets to your entered events. These offsets represent:

*   **Original Date**: The date and time you remember an event occurring.
*   **Shifted Date**: Where that event *might* have landed if a minor temporal ripple nudged it slightly forward or backward.
*   **Echo Date**: A faint, distant echo of the event, appearing further in the past, suggesting a recurring pattern or a premonition.

It's a tool for reflection, a conversation starter, and a gentle reminder that even in chaos, there's a pattern to be found – or invented!

## How to Run

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-chrono-compass
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

4.  **To build for production:**
    ```bash
    npm run build
    ```
    This will create a `build` directory with optimized static files.

## How to Use

1.  **Enter Event Details**: In the input form, provide a name for your event (e.g., "Found the last can of beans", "Encountered a friendly mutant") and the date and time it occurred.
2.  **Add Event**: Click the "Add Event" button.
3.  **Observe**: The event will appear in the Chrono-Compass display, showing its original date, its playfully 'shifted' date, and its 'echoed' date. Reflect on the new perspectives!

## Project Structure

```
. 
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.js
│   ├── ChronoCompass.js
│   ├── EventInput.js
│   ├── index.js
│   └── styles.css
└── tests/
    ├── App.test.js
    └── ChronoCompass.test.js
```
