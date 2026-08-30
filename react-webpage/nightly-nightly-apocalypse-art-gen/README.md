## Nightly Apocalypse Art Generator

This utility generates whimsical and thought-provoking art prompts inspired by the ApocalypsAI theme. It's designed to spark creativity for artists, writers, or anyone looking for a unique artistic challenge.

### How it Works

The web interface presents a series of dropdowns and input fields, allowing users to combine various elements to construct a unique art prompt. These elements include themes, styles, subjects, and apocalyptic scenarios.

### Features

*   **Thematic Combinations**: Mix and match different apocalyptic themes with artistic styles.
*   **Subject Customization**: Specify unique subjects for your artwork.
*   **Random Prompt Generation**: A "Surprise Me!" button to generate a completely random prompt.
*   **Save Prompt**: Option to save your favorite generated prompts.

### Getting Started

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```

2.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-apocalypse-art-gen
    ```

3.  **Install dependencies**:
    ```bash
    npm install
    ```

4.  **Start the development server**:
    ```bash
    npm start
    ```

5.  **Open your browser** to `http://localhost:3000` (or the port specified by `npm start`).

### Usage

*   Select options from the dropdown menus for "Apocalypse Theme", "Art Style", and "Subject".
*   Optionally, enter a specific "Custom Subject" or "Additional Details".
*   Click "Generate Prompt" to see your creation.
*   Click "Surprise Me!" for a random prompt.
*   Click "Save Prompt" to add the current prompt to your saved list.

### Development

This project was bootstrapped with Create React App.

#### Available Scripts

In the project directory, you can run:

`npm start`
    Runs the app in the development mode.
    Open http://localhost:3000 to view it in the browser.

`npm test`
    Launches the test runner in interactive watch mode.

`npm run build`
    Builds the app for production to the `build` folder.

### Tests

Unit tests are included to ensure the core functionality of prompt generation and state management works as expected. These tests are deterministic and do not require external dependencies.
