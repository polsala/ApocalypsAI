# Nightly Beacon Signal Visualizer

## Summary

The Nightly Beacon Signal Visualizer is a whimsical, interactive web utility designed to transform any text input (a 'beacon signal') into a unique, mesmerizing visual pattern. It's a fun way for the community to generate abstract visual representations of messages, moods, or just random thoughts, fostering a sense of shared, albeit abstract, communication.

## How it Works

1.  **Input a Signal**: Users type any text into the input field.
2.  **Generate Parameters**: The text is deterministically hashed to generate a set of visual parameters (e.g., number of rings, color hues, rotation speed, flicker intensity).
3.  **Visualize**: These parameters drive an SVG-based animation, creating a unique 'beacon signal' visualization.

Each unique text input will produce a consistent, unique visual output, allowing for a form of abstract, shared 'signal' recognition within the community.

## Installation & Usage

To run this utility, you need Node.js and npm (or yarn) installed.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-beacon-signal-visualizer
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```

3.  **Start the development server**:
    ```bash
    npm start
    # or yarn start
    ```

    This will open the application in your browser, usually at `http://localhost:3000`.

4.  **Interact**: Type your 'beacon signal' into the input box and watch the visualization change in real-time.

## Development

### Project Structure

```
. 
├── README.md
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.css
│   ├── App.js
│   ├── index.js
│   └── SignalVisualizer.js
└── tests/
    ├── App.test.js
    └── SignalVisualizer.test.js
```

### Running Tests

To run the automated tests:

```bash
npm test
# or yarn test
```

Tests are written using React Testing Library and Jest, ensuring the core logic and component rendering behave as expected.
