# Nightly Temporal Echo Visualizer

## Summary
This utility provides an interactive web interface to simulate how a given piece of text might 'echo' and 'distort' across various temporal shifts. Input your message, and watch as it's playfully transformed into different 'echoes' – from subtle whispers to chaotic void distortions. It's perfect for creative brainstorming, generating whimsical text variations, or simply pondering the ephemeral nature of communication.

## Features
- Input any text and generate multiple 'temporal echoes'.
- Different distortion levels (Whisper, Temporal Shift, Void Echo) apply unique transformations.
- Interactive UI built with React.

## Installation & Setup
To run this utility, you'll need Node.js and npm (or yarn) installed on your system.

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-temporal-echo-viz
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    # or yarn install
    ```
3.  **Start the development server:**
    ```bash
    npm start
    # or yarn start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

## Usage
1.  Once the application is running, you will see an input field labeled "Enter your message to echo...".
2.  Type or paste the text you wish to transform.
3.  Click the "Generate Echoes" button.
4.  The application will display several 'echoes' of your original message, each with a different simulated temporal distortion.

## Project Structure
```
nightly-temporal-echo-viz/
├── public/
│   └── index.html
├── src/
│   ├── App.css
│   ├── App.js
│   ├── EchoDisplay.js
│   ├── EchoGenerator.js
│   └── index.js
├── tests/
│   └── EchoGenerator.test.js
├── package.json
└── README.md
```

## Technologies Used
- React
- JavaScript (ES6+)
- CSS
- Jest (for testing)

## Contributing
Feel free to explore the `EchoGenerator.js` file to understand and even expand upon the existing distortion algorithms. New 'temporal filters' are always welcome!
