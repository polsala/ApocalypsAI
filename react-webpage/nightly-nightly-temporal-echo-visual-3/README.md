# Nightly Temporal Echo Visualizer

An interactive React web dashboard to visualize detected temporal echoes and anomalies across a timeline. This utility provides a whimsical yet functional interface to monitor temporal stability, displaying various "echo types" with distinct visual cues.

## Features

*   **Echo Visualization:** Displays a list of detected temporal echoes with their timestamp, location, type, magnitude, and a brief description.
*   **Whimsical Echo Types:** Categorizes echoes into "Whisper", "Ripple", "Glitch", and "Paradox", each with a unique emoji icon.
*   **Mock Data Integration:** Comes with mock data for immediate demonstration and testing.

## Installation and Usage

To run this utility, you need Node.js and npm installed.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-temporal-echo-visualizer
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

## Running Tests

To run the automated tests:

```bash
npm test
```

## Project Structure

```
.
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.css
│   ├── App.js
│   ├── data/
│   │   └── mockEchoData.js
│   └── index.js
└── tests/
    └── App.test.js
```
