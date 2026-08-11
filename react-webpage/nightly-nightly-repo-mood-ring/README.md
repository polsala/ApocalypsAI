# nightly-repo-mood-ring

A whimsical React web interface designed to visualize the current "mood" or "vibe" of the ApocalypsAI repository. By analyzing recent (mocked) GitHub activity, this tool assigns a color and description, much like a digital mood ring, giving the community a quick glance at the collective energy.

## Features

*   **Whimsical Mood Visualization:** Displays the repository's mood using a color-changing "mood ring" and descriptive text.
*   **Activity-Based Analysis:** Calculates mood based on a simplified analysis of recent issue and PR titles (mocked data).
*   **User Vibe Check:** Allows users to input their own personal "vibe check" for the day.
*   **Self-Contained React App:** A standalone web application built with React.

## Moods Explained

The mood ring cycles through various states based on the detected activity:

*   **Serene Green:** The void hums with positive energy! Lots of features, enhancements, and successful fixes.
*   **Calm Blue:** Steady progress. The void is in a state of focused maintenance, refactoring, and documentation updates.
*   **Energetic Yellow:** A flurry of activity! The void is buzzing with mixed signals – new features alongside some minor issues.
*   **Fiery Red:** Warning! Critical issues detected. The void is agitated with urgent bugs and system failures.
*   **Mysterious Purple:** The void is quiet, contemplating its next move. Low activity or a balanced mix of minor items.

## How to Run

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-repo-mood-ring
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

## How to Develop

The project was bootstrapped with Create React App. You can find more information in the [Create React App documentation](https://create-react-app.dev/docs/getting-started).

## How to Test

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-repo-mood-ring
    ```
2.  **Run the tests:**
    ```bash
    npm test
    ```
    This will execute the unit tests using Jest and React Testing Library. The `src/api.js` module is mocked to ensure tests are deterministic and do not rely on external network requests.

## Project Structure

```
.
├── README.md
├── package.json
├── src/
│   ├── App.css
│   ├── App.js
│   ├── MoodRing.css
│   ├── MoodRing.js
│   ├── api.js             # Mocked GitHub activity data source
│   ├── index.css          # Minimal global styles
│   └── index.js           # React app entry point
└── tests/
    └── App.test.js        # Unit tests for the App component
```
