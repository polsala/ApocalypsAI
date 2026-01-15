## Nightly Apocalypse Dashboard

This is a whimsical React-based dashboard designed to provide a lighthearted overview of the current state of the apocalypse. It visualizes various 'apocalyptic metrics' and offers survival tips to keep spirits high.

### Features

*   **Whimsical Metrics:** Displays fun, fictional metrics like 'Zombie Proximity Index', 'Mutant Mutation Rate', and 'Resource Scarcity Level'.
*   **Survival Tips:** Offers daily survival advice, ranging from practical to absurd.
*   **Interactive Elements:** Hovering over metrics reveals more details or humorous anecdotes.
*   **Customizable Themes:** (Future enhancement) Allow users to choose their preferred apocalyptic aesthetic.

### Getting Started

1.  **Prerequisites:** Node.js and npm (or yarn) installed.
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```
3.  **Navigate to the utility:**
    ```bash
    cd utils/nightly-apocalypse-dashboard
    ```
4.  **Install dependencies:**
    ```bash
    npm install
    ```
5.  **Start the development server:**
    ```bash
    npm start
    ```
    This will open the dashboard in your browser.

### Running Tests

To run the unit tests:

```bash
npm test
```

### Structure

*   `README.md`: This file.
*   `src/App.js`: The main React component for the dashboard.
*   `src/components/MetricCard.js`: A reusable component for displaying individual metrics.
*   `src/components/SurvivalTip.js`: A component for displaying daily survival tips.
*   `src/data/mockMetrics.js`: Mock data for the apocalyptic metrics.
*   `src/data/mockTips.js`: Mock data for survival tips.
*   `tests/App.test.js`: Unit tests for the main App component.
*   `tests/MetricCard.test.js`: Unit tests for the MetricCard component.
