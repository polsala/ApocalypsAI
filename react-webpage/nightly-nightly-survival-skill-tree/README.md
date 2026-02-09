# Nightly Survival Skill Tree

## Summary
This utility is an interactive React web application designed to help survivors visualize and track their personal skill progression in a whimsical, post-apocalyptic skill tree format. It allows users to 'unlock' skills, see their prerequisites, and understand their path to becoming a true wasteland master.

## Features
*   **Interactive Skill Tree**: Click to unlock or lock skills.
*   **Prerequisite Tracking**: Skills can only be unlocked if their prerequisites are met.
*   **Whimsical Theme**: Post-apocalyptic survival skills presented in a fun, game-like interface.
*   **Persistence**: Your unlocked skills are saved in local storage, so your progress isn't lost.
*   **Self-Contained**: Easy to run locally with standard Node.js/npm tools.

## How to Run
1.  **Prerequisites**: Ensure you have Node.js (v14 or higher recommended) and npm (or yarn) installed.
2.  **Navigate**: Change into the `nightly-survival-skill-tree` directory.
3.  **Install Dependencies**: Run `npm install` (or `yarn install`).
4.  **Start the Application**: Run `npm start` (or `yarn start`).
    *   This will open the application in your default web browser, usually at `http://localhost:3000`.

## How to Use
Once the application is running:
1.  **View Skills**: Browse the list of available survival skills. Skills with a cyan border are currently unlockable.
2.  **Unlock Skills**: Click on a skill's 'Unlock' button to attempt to unlock it. If the skill has prerequisites, they must be unlocked first.
3.  **Track Progress**: See which skills you've mastered ('Mastered!' button) and which ones are still locked.
4.  **Reset Progress**: To reset all skills, you can clear your browser's local storage for `http://localhost:3000`.

## Project Structure
```
nightly-survival-skill-tree/
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.css
│   ├── App.js
│   ├── index.css
│   ├── index.js
│   ├── SkillNode.css
│   ├── SkillNode.js
│   ├── SkillTree.css
│   └── SkillTree.js
└── tests/
    └── App.test.js
```

## Automated Tests
To run the automated tests for this utility:
1.  **Navigate**: Change into the `nightly-survival-skill-tree` directory.
2.  **Run Tests**: Execute `npm test` (or `yarn test`).

Tests are deterministic and offline, using `@testing-library/react` and Jest to simulate user interactions and verify component behavior. Local storage interactions are mocked to ensure consistent test results.
