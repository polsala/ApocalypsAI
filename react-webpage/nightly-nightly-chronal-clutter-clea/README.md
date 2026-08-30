# Nightly Chronal Clutter Cleaner

The ApocalypsAI Nightly Integrator presents the "Chronal Clutter Cleaner" – a whimsical yet practical web dashboard designed to help the community identify and prioritize digital detritus that accumulates over time in their projects. Think of it as a temporal dust-bunny hoover for your codebase and task lists!

## What is Chronal Clutter?

Chronal clutter refers to the digital remnants that, while once useful, now obscure clarity and efficiency. This includes:
- Stale Git branches
- Long-forgotten issues or pull requests
- Unused dependencies
- Outdated documentation sections
- Unfinished tasks that have lingered for eons

## How it Works (Conceptually)

This utility provides a visual interface to categorize and manage these "clutter items." While this initial version uses mock data, the vision is for it to integrate with various project management tools (GitHub, Jira, etc.) and code repositories to automatically detect and present actionable insights.

## Features

- **Clutter Visualization:** See your digital detritus at a glance.
- **Categorization:** Items are categorized by type (e.g., 'Branch', 'Issue', 'Dependency').
- **Prioritization:** Each item has a 'Temporal Weight' indicating its age/staleness.
- **Interactive Filtering:** Filter clutter by type or temporal weight.
- **Actionable Insights:** (Future) Links to directly address the clutter.

## Installation and Usage

This is a React application.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-chronal-clutter-cleaner
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

## Project Structure

```
.
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.js              # Main application component
│   ├── index.js            # React entry point
│   ├── ClutterItem.js      # Component for displaying a single clutter item
│   └── mockClutter.js      # Mock data for demonstration and testing
└── tests/
    ├── App.test.js         # Tests for the main App component
    └── ClutterItem.test.js # Tests for the ClutterItem component
```

## Running Tests

To run the automated tests:

```bash
cd react-webpage/nightly-chronal-clutter-cleaner
npm test
```
