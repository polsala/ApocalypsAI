# Nightly Whisper Cloud Visualizer

An interactive React web application that generates a whimsical word cloud from user-provided text, highlighting the most frequent "whispers" or themes. Perfect for quickly grasping the essence of a long log, a collection of survivor notes, or even just your own rambling thoughts.

## Features

*   **Text Input:** Paste or type your text.
*   **Dynamic Word Cloud:** See the most frequent words appear larger.
*   **Whimsical Styling:** A simple, clean interface to focus on the "whispers".

## How to Run

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-whisper-cloud-visualizer
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    # or
    yarn install
    ```
3.  **Start the development server:**
    ```bash
    npm start
    # or
    yarn start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

## How to Use

1.  Type or paste your text into the provided textarea.
2.  Click the "Generate Whispers" button.
3.  Observe the word cloud generated below, where larger words indicate higher frequency.

## Project Structure

```
.
├── README.md
├── package.json
├── public/
│   └── index.html
└── src/
    ├── App.css
    ├── App.js
    └── index.js
└── tests/
    └── App.test.js
```

## Automated Tests

To run the tests:

```bash
cd react-webpage/nightly-whisper-cloud-visualizer
npm test
# or
yarn test
```
