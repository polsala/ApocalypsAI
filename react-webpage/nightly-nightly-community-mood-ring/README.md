# Nightly Community Mood Ring

The Nightly Community Mood Ring is a whimsical React web application designed to help communities track and visualize their collective emotional state. In the face of the apocalypse, understanding morale is crucial! This tool allows individuals to log their daily mood using a selection of fun, post-apocalyptic themed emojis and descriptions. The app then displays recent mood entries and a simple summary, helping community leaders and members get a quick pulse on well-being.

## Features

*   **Whimsical Mood Selection**: Choose from a set of unique, apocalypse-appropriate moods.
*   **Daily Mood Logging**: Easily record your mood for the day with a timestamp.
*   **Recent Mood History**: View a list of the most recent mood submissions.
*   **Simple Mood Summary**: Get an overview of the most frequently logged moods.
*   **Local Storage Persistence**: Moods are saved in your browser's local storage, persisting across sessions.

## How to Run

This is a standard React application. You'll need Node.js and npm (or yarn) installed.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-community-mood-ring
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

4.  **Build for production (optional):**
    ```bash
    npm run build
    # or yarn build
    ```
    This will create a `build` directory with the optimized production-ready files.

## Usage

1.  **Select your mood**: Choose one of the whimsical mood options.
2.  **Log your mood**: Click the "Log My Mood" button. Your mood will be recorded with the current timestamp.
3.  **View History**: See your recent mood entries in the "Recent Moods" section.
4.  **Check Summary**: The "Mood Summary" provides insights into the overall community sentiment based on logged data.

## Development Notes

The application uses React's functional components and hooks. Mood data is stored in `localStorage`. For a real-world deployment, you might integrate this with a backend API for shared community data.

## Tests

To run the automated tests:

```bash
npm test
# or yarn test
```
