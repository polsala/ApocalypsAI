# Nightly Chrono-Choreographer

## Overview

The `nightly-chrono-choreographer` is a whimsical-yet-useful React web application designed to help survivors (or just busy individuals) organize their daily 'apocalyptic' tasks. Whether you're fortifying your bunker, scavenging for temporal anomalies, or simply remembering to feed your pet sentient slime, this tool provides an interactive calendar to keep your schedule in check. Tasks can be added, assigned to specific days, marked as complete, and persist across browser sessions using local storage.

## Features

*   **Task Management:** Add new tasks with whimsical names.
*   **Day Assignment:** Assign tasks to any day of the week.
*   **Status Tracking:** Mark tasks as 'Pending' or 'Completed'.
*   **Persistence:** All tasks are saved and loaded from your browser's local storage.
*   **Interactive UI:** A simple, clean interface built with React.

## Installation and Setup

To run this utility, you need Node.js and npm (or yarn) installed.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-chrono-choreographer
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

1.  **Add a New Task:** Use the input field and 'Add Task' button to create a new task. It will initially appear in the 'Unassigned Tasks' list.
2.  **Assign a Task:** Click on an unassigned task. A dropdown will appear allowing you to select a day of the week to assign it to.
3.  **Mark as Complete:** Click on a task assigned to a day to toggle its completion status.
4.  **Clear Completed Tasks:** Use the 'Clear Completed' button to remove all tasks marked as 'Completed'.

## Project Structure

```
nightly-chrono-choreographer/
├── public/
│   └── index.html      # Main HTML file
├── src/
│   ├── App.css         # Styling for the application
│   ├── App.js          # Main React component, handles state and logic
│   ├── TaskCalendar.js # Component for displaying the weekly calendar
│   ├── TaskItem.js     # Component for individual task rendering
│   └── index.js        # React app entry point
├── package.json        # Project dependencies and scripts
├── .gitignore
└── README.md
```

## Testing

Tests are written using Jest and React Testing Library. They ensure the core functionality, such as task management and persistence, works as expected.

1.  **Run tests:**
    ```bash
    npm test
    # or yarn test
    ```

## Technologies Used

*   React
*   JavaScript (ES6+)
*   CSS
*   Node.js / npm
*   Jest / React Testing Library
