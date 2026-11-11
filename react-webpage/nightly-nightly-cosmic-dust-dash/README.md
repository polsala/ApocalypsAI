# Nightly Cosmic Dust Collector Dashboard

This utility provides an interactive React web dashboard to visualize the "cosmic dust" collected by the ApocalypsAI agents. "Cosmic dust" represents key GitHub activity metrics such as repository stars, commits, and issues, presented in a whimsical, gamified interface. It allows the community to observe the project's growth and agent activity over time.

## Features

*   **Overview Metrics:** Displays total mock stars, commits, and issues.
*   **Time-Series Visualization:** A simple bar chart (mocked with divs) showing daily "dust" collection.
*   **Top Dust Collectors:** Lists mock agent activity.
*   **Time Range Selection:** Filter data for the last 7 or 30 days.

## Usage

To run this React application:

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-cosmic-dust-dash
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Start the development server:**
    ```bash
    npm start
    ```
    This will open the dashboard in your browser, usually at `http://localhost:3000`.

4.  **Build for production (optional):**
    ```bash
    npm run build
    ```
    This creates a `build` directory with optimized static files.

## Project Structure

```
.
├── README.md
├── package.json
├── public/
│   └── index.html          # Main HTML file
├── src/
│   ├── App.js              # Main React component
│   ├── index.js            # React entry point
│   ├── components/
│   │   └── Dashboard.js    # Dashboard layout and logic
│   ├── data/
│   │   └── mockData.js     # Mock data for visualization
│   └── App.css             # Basic styling
└── tests/
    └── App.test.js         # Automated tests for the App component
```

## Automated Tests

Tests are implemented using Jest and React Testing Library. To run them:

```bash
npm test
```

### Mock Rationale

All data displayed in the dashboard is generated from `src/data/mockData.js`. This ensures that the utility is entirely self-contained, deterministic, and can be tested offline without relying on external API calls or network connectivity. The mock data simulates realistic GitHub activity metrics for demonstration and testing purposes.
