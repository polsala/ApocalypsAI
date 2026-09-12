## Nightly Apocalypse Dashboard

This is a whimsical React-based web application designed to provide a visual overview of the ApocalypsAI project's status. It aims to be both informative and fun, reflecting the project's "anarchy with discipline" philosophy.

### Features

*   **Agent Status Overview**: A colorful display of active and idle agents.
*   **Utility Generation Tracker**: Visualizes the rate and types of utilities being generated.
*   **Workflow Health Monitor**: A simple indicator of recent GitHub Actions workflow success/failure rates.
*   **Whimsical Elements**: Incorporates fun animations and thematic elements.

### Getting Started

1.  **Prerequisites**: Node.js and npm/yarn installed.
2.  **Installation**: 
    ```bash
    cd utils/nightly-apocalypse-dashboard
    npm install
    ```
3.  **Running the Development Server**: 
    ```bash
    npm start
    ```
    This will launch the dashboard in your browser, typically at `http://localhost:3000`.

### Building for Production

```bash
    npm run build
    ```

This will create a `build` folder with the optimized static assets.

### Testing

To run the unit tests:

```bash
    npm test
    ```

### Structure

*   `public/`: Static assets.
*   `src/`:
    *   `App.js`: Main application component.
    *   `components/`: Reusable UI components (e.g., `AgentStatusCard.js`, `WorkflowIndicator.js`).
    *   `utils/`: Helper functions (e.g., mock data generation).
    *   `App.css`: Global styles.
*   `tests/`:
    *   `App.test.js`: Basic test for the main App component.
    *   `components/AgentStatusCard.test.js`: Tests for individual components.
