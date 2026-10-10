# Nightly Chrono-Chatter Visualizer

An interactive web utility to simulate and visualize how a short message might be interpreted, rephrased, or distorted by various post-apocalyptic factions. Ever wonder how "The supplies are low" sounds to a Vault Dweller versus a Wasteland Scavenger? This tool provides a whimsical glimpse into potential communication breakdowns across timelines and ideologies.

## Features

*   Input a short message.
*   See immediate "echoes" from predefined factions, each with a unique linguistic style.
*   Interactive UI built with React.

## Installation

1.  Navigate to the utility directory:
    ```bash
    cd react-webpage/nightly-chrono-chatter-viz
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

1.  Start the development server:
    ```bash
    npm start
    ```
    This will typically open the application in your browser at `http://localhost:3000`.
2.  Type a message into the input field.
3.  Click "Generate Echoes" (or press Enter) to see how different factions might interpret your message.

## Development

The project was bootstrapped with Create React App.

### Available Scripts

In the project directory, you can run:

*   `npm start`: Runs the app in development mode.
*   `npm test`: Launches the test runner.
*   `npm run build`: Builds the app for production to the `build` folder.

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
│   ├── FactionEcho.js
│   ├── index.css
│   └── index.js
│   └── utils/
│       └── echoGenerator.js
└── tests/
    ├── App.test.js
    ├── FactionEcho.test.js
    └── echoGenerator.test.js
```
