# Nightly Survival Skill Tree Planner

An interactive React web application designed to help survivors plan and visualize their post-apocalyptic skill progression. Whether you're focusing on scavenging, crafting, combat, or even temporal manipulation, this tool allows you to map out your ideal skill tree, track learned abilities, and understand prerequisites.

## Features

*   **Interactive Skill Tree:** Click on skill nodes to "learn" them.
*   **Prerequisite Tracking:** Skills can have prerequisites that must be learned first.
*   **Visual Feedback:** Clearly see learned skills and available next steps.
*   **Customizable Data:** Easily modify `src/data/skills.js` to create your own skill sets.

## How to Run

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-skill-tree-planner
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

## How to Test

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-skill-tree-planner
    ```
2.  **Run tests:**
    ```bash
    npm test
    ```
    This will execute the Jest tests for the React components.

## Project Structure

```
.
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   ├── index.css
│   ├── SkillNode.js
│   ├── SkillNode.css
│   ├── SkillTree.js
│   ├── SkillTree.css
│   └── data/
│       └── skills.js
└── tests/
    ├── App.test.js
    └── SkillTree.test.js
```
