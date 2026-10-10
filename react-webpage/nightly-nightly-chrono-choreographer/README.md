# Nightly Chrono-Choreographer

## Whimsical Task Management for the Post-Apocalyptic Planner

The `nightly-chrono-choreographer` is a delightful React web application designed to transform your mundane daily tasks into an engaging 'temporal dance sequence'. Instead of just a list, visualize your day's flow, adjust your 'choreography', and bring a touch of whimsy to your survival planning.

### Features

*   **Task Input**: Easily add new tasks with a name and an estimated duration.
*   **Temporal Dance Floor**: A visual representation of your day, where each task is a 'dance move' with a length proportional to its duration.
*   **Reorder Choreography**: Adjust the sequence of your tasks using simple up/down arrows, perfecting your daily routine.
*   **Persistence**: Your task choreography is saved locally in your browser, so your dance moves are remembered.
*   **Whimsical Design**: A lighthearted interface to make task management less of a chore and more of a performance.

### How to Run

This utility is a standard React application. To run it locally:

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-chrono-choreographer
    ```
2.  **Install dependencies** (if you don't have `npm` or `yarn`, you'll need to install Node.js first):
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

### How to Use

1.  **Add a Task**: Use the input fields to enter a task name (e.g., "Scavenge for rations") and its estimated duration in minutes (e.g., "60"). Click "Add Task".
2.  **View Choreography**: Your tasks will appear in the list and on the 'Temporal Dance Floor' below.
3.  **Reorder Tasks**: Use the "Up" and "Down" arrows next to each task to change its position in your daily sequence.
4.  **Remove Tasks**: Click the "X" button to remove a task from your choreography.
5.  **Persistence**: Your tasks are automatically saved and will reappear if you close and reopen the browser tab.

### Development and Testing

To run the automated tests:

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-chrono-choreographer
    ```
2.  **Run tests**:
    ```bash
    npm test
    # or yarn test
    ```
    This will execute the tests defined in `tests/App.test.js`.
