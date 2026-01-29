# Nightly Aura Analyzer

## Overview

The Nightly Aura Analyzer is a whimsical-yet-useful React web application designed to help the community quickly gauge the emotional tone of text inputs. Whether it's a survivor's log entry, a broadcast message, or a snippet of intercepted chatter, this tool processes the text and visualizes its underlying sentiment as a vibrant 'aura' color.

It's like a mood ring for your text, providing a quick, intuitive read on the emotional landscape of the post-apocalyptic world.

## Features

*   **Text Input**: Simple text area for entering any message.
*   **Sentiment Analysis**: Basic, rule-based sentiment detection (positive, neutral, negative).
*   **Aura Visualization**: Displays a dynamic color 'aura' around the input area, changing based on the detected sentiment.
*   **Whimsical Feedback**: Provides a short, descriptive phrase for the detected mood.

## Setup and Running

To run this utility, you'll need Node.js and npm (or yarn) installed.

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-aura-analyzer
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
    This will typically open the application in your browser at `http://localhost:3000`.

4.  **Build for production (optional)**:
    ```bash
    npm run build
    # or yarn build
    ```
    This will create a `build` directory with the optimized production-ready files.

## Usage

1.  Open the application in your web browser.
2.  Type or paste any text into the provided text area.
3.  Observe the 'aura' color and the mood description change dynamically as you type, reflecting the sentiment of your input.

## Development

### Project Structure

```
nightly-aura-analyzer/
├── public/
│   └── index.html
├── src/
│   ├── App.css
│   ├── App.js
│   ├── index.js
│   └── SentimentAnalyzer.js
├── package.json
└── README.md
```

### Testing

To run the automated tests:

```bash
npm test
# or yarn test
```

Tests are written using Jest and React Testing Library. They cover both the React component's behavior and the sentiment analysis logic, using mocks for deterministic results.
