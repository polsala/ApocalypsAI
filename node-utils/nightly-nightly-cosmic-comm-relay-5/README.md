# Nightly Cosmic Comm Relay

A whimsical Node.js utility that simulates the unpredictable nature of intergalactic communication. It introduces random delays and message corruption, perfect for testing resilience or just for fun.

## Features

*   Simulates variable communication latency.
*   Introduces random character corruption in messages.
*   Cross-platform compatibility (Node.js).

## Installation

```bash
npm install @polsala/nightly-cosmic-comm-relay
```

## Usage

```javascript
const { CosmicCommRelay } = require('@polsala/nightly-cosmic-comm-relay');

const relay = new CosmicCommRelay({
  baseDelayMs: 500, // Base delay in milliseconds
  delayVariance: 200, // Max additional delay
  corruptionChance: 0.1 // Probability of a character being corrupted
});

async function sendMessage(message) {
  console.log(`Sending: "${message}"`);
  const receivedMessage = await relay.send(message);
  console.log(`Received: "${receivedMessage}"`);
}

(async () => {
  await sendMessage("Greetings from Sector 7G!");
  await sendMessage("The nebula is particularly vibrant today.");
  await sendMessage("Report status of the warp core.");
})();
```

## Configuration Options

*   `baseDelayMs` (number): The base delay for messages in milliseconds. Defaults to 500.
*   `delayVariance` (number): The maximum additional random delay in milliseconds. Defaults to 200.
*   `corruptionChance` (number): The probability (0.0 to 1.0) that any given character in a message will be corrupted. Defaults to 0.1.

## Development

To run the tests locally:

```bash
npm install
npm test
```
