# Nightly Repo Vibe Visualizer

## Summary
The Nightly Repo Vibe Visualizer is a whimsical React web application designed to give you an at-a-glance understanding of the 'mood' or 'vibe' of your repository's recent activity. By analyzing commit messages, PR titles, and issue comments, it assigns a dominant 'vibe' (e.g., Optimistic, Chaotic, Serene, Mysterious) and displays it visually.

## Features
- Analyzes text contributions to determine a repository's current 'vibe'.
- Displays the vibe using a simple, color-coded visualizer.
- Easy to set up and run locally.

## How it Works
The core logic resides in `src/VibeAnalyzer.js`. It scans input text for keywords associated with different 'vibe' categories:
- **Optimistic**: `feat`, `add`, `new`, `improve`, `enhance`, `release`
- **Chaotic**: `fix`, `bug`, `error`, `break`, `urgent`, `hotfix`
- **Serene**: `refactor`, `clean`, `docs`, `style`, `chore`, `test`
- **Mysterious**: `update`, `adjust`, `tweak`, `change`, `revert` (default/neutral if no other strong vibe)

The category with the highest keyword count determines the dominant vibe. In case of a tie, a predefined priority order (Optimistic > Chaotic > Serene > Mysterious) ensures deterministic output.

## Setup and Running

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-repo-vibe-visualizer
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the application:**
    ```bash
    npm start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

## Development

### Available Scripts
In the project directory, you can run:

- `npm start`: Runs the app in development mode.
- `npm test`: Launches the test runner.
- `npm run build`: Builds the app for production to the `build` folder.

### Customizing Vibe Analysis
You can modify the `VIBE_KEYWORDS` object in `src/VibeAnalyzer.js` to adjust how vibes are detected or add new categories.

## Example Usage (Mocked Data)
Currently, the application uses mocked data to demonstrate its functionality. In a real-world scenario, you would integrate it with a GitHub API client or similar to fetch actual commit messages and PR titles.

```javascript
// Example of data that would be fed to VibeAnalyzer
const recentContributions = [
  "feat: add new user authentication module",
  "fix(bug): resolve critical database connection issue",
  "docs: update README with new setup instructions",
  "chore: clean up unused dependencies",
  "refactor: simplify data fetching logic",
  "urgent: hotfix for production outage",
  "style: format code with prettier",
  "update: dependencies",
  "tweak: UI spacing"
];
// This would result in a 'Chaotic' vibe due to 'fix', 'bug', 'urgent', 'hotfix'
```
