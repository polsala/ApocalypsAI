# Nightly Cosmic Comm Relay

A whimsical Node.js utility that simulates the unpredictable nature of intergalactic communication. It introduces random delays and message corruption, perfect for testing resilient communication protocols or just for fun.

## Features

*   Simulates variable communication delays.
*   Introduces random message corruption (character substitution, deletion, insertion).
*   Cross-platform compatibility (Node.js).

## Installation

```bash
npm install @polsala/nightly-cosmic-comm-relay
```

## Usage

```javascript
const cosmicRelay = require('@polsala/nightly-cosmic-comm-relay');

async function sendMessage(message, destination) {
  console.log(`Sending message to ${destination}: "${message}"`);
  try {
    const receivedMessage = await cosmicRelay.send(message, {
      delayRange: [500, 3000], // milliseconds
      corruptionChance: 0.3 // 30% chance of corruption
    });
    console.log(`Received at ${destination}: "${receivedMessage}"`);
  } catch (error) {
    console.error(`Transmission failed: ${error.message}`);
  }
}

sendMessage("Greetings, fellow sentient beings!", "Alpha Centauri Outpost");
sendMessage("Urgent: Supplies needed!", "Nebula Station 7");
```

## API

### `cosmicRelay.send(message: string, options?: { delayRange: [number, number], corruptionChance: number }): Promise<string>`

*   `message`: The original message string to send.
*   `options`: An optional object to configure the relay behavior.
    *   `delayRange`: An array `[min, max]` specifying the minimum and maximum delay in milliseconds. Defaults to `[100, 2000]`.
    *   `corruptionChance`: A number between 0 and 1 representing the probability of message corruption. Defaults to `0.1` (10%).

Returns a Promise that resolves with the potentially corrupted message, or rejects if an unrecoverable error occurs (though this implementation is designed to be resilient).

## Development & Testing

Run tests using:

```bash
npm test
```
