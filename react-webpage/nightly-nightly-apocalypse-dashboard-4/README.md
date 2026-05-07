## ApocalypsAI Dashboard

This is a whimsical React-based web application designed to provide a visual overview of the ApocalypsAI project's utility status and their perceived 'apocalypse readiness'. It aims to be both informative and entertaining, showcasing the diverse range of utilities developed by the project.

### Features

*   **Utility Overview**: Lists all available ApocalypsAI utilities categorized by their classifier.
*   **Readiness Meter**: A visual indicator for each utility, suggesting its 'apocalypse readiness' based on a mock status.
*   **Whimsical Touches**: Fun animations and thematic elements to keep the user engaged.

### Getting Started

1.  **Prerequisites**: Node.js and npm (or yarn) installed.
2.  **Clone the repository**: `git clone https://github.com/polsala/ApocalypsAI.git`
3.  **Navigate to the utility directory**: `cd ApocalypsAI/react-webpage/nightly-apocalypse-dashboard`
4.  **Install dependencies**: `npm install` (or `yarn install`)
5.  **Start the development server**: `npm start` (or `yarn start`)

This will launch the dashboard in your browser, typically at `http://localhost:3000`.

### Building for Production

To create a production-ready build:

1.  Run `npm run build` (or `yarn build`).

This will generate a `build` folder containing the optimized static assets.

### Testing

To run the unit tests:

1.  Run `npm test` (or `yarn test`).

### Structure

*   `public/`: Static assets like `index.html`.
*   `src/`: React components and application logic.
    *   `components/`: Reusable UI components.
    *   `App.js`: Main application component.
    *   `index.js`: Entry point.
    *   `utils/`: Helper functions (e.g., mock data generation).
*   `tests/`: Unit tests for components and logic.
