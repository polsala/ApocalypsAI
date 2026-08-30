# Nightly Cosmic Comm Relay

A whimsical Node.js utility that simulates the unpredictable nature of interstellar communication. It introduces random delays and potential message corruption, perfect for adding a touch of cosmic chaos to your development or testing workflows.

## Features

*   Simulates variable communication delays between planets.
*   Introduces random message corruption (character substitution, deletion, insertion).
*   Configurable parameters for delay, corruption probability, and corruption type.
*   Cross-platform compatibility via Node.js.

## Installation

```bash
npm install @polsala/nightly-cosmic-comm-relay
```

## Usage

### Command Line Interface (CLI)

Run the utility directly from your terminal:

```bash
npx @polsala/nightly-cosmic-comm-relay "Hello, distant star!" --delay 500 --corruption 0.1 --type substitute
```

**Arguments:**

*   `message` (required): The message to send.
*   `--delay` (optional, default: 100ms): The base delay in milliseconds before processing.
*   `--corruption` (optional, default: 0.05): The probability of message corruption (0.0 to 1.0).
*   `--type` (optional, default: 'substitute'): The type of corruption to apply. Options: `substitute`, `delete`, `insert`.

### Programmatic Usage

```javascript
const { sendCosmicMessage } = require('@polsala/nightly-cosmic-comm-relay');

async function communicate() {
    const originalMessage = "Greetings from Earth!";
    const planet = "Xylos";

    console.log(`Sending message to ${planet}...`);

    try {
        const receivedMessage = await sendCosmicMessage(originalMessage, {
            delay: 750, // ms
            corruptionProbability: 0.15,
            corruptionType: 'insert'
        });
        console.log(`Received from ${planet}: "${receivedMessage}"`);
    } catch (error) {
        console.error(`Communication failed: ${error.message}`);
    }
}

communicate();
```

## How it Works

The utility uses Node.js's `setTimeout` to simulate delays and a series of random checks to introduce corruption. Different corruption types modify the message in unique ways:

*   **Substitute**: Replaces random characters with other characters.
*   **Delete**: Removes random characters.
*   **Insert**: Inserts random characters at random positions.

## Development & Testing

This project uses Jest for testing. To run tests:

```bash
npm install
npm test
```
