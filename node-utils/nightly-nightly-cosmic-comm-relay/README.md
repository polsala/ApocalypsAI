## Nightly Cosmic Comm Relay

This utility simulates sending messages across vast cosmic distances, introducing whimsical delays and static effects. It's a fun way to add a bit of flavor to inter-process communication or just to send a message to yourself in the future (with a twist!).

### Features

*   **Simulated Cosmic Delay**: Messages take time to "travel".
*   **Cosmic Static**: Introduces random "noise" to messages.
*   **Configurable Distance**: Adjust the perceived distance for varied delays.
*   **Cross-Platform**: Runs anywhere Node.js is installed.

### Installation

```bash
npm install @polsala/nightly-cosmic-comm-relay
```

### Usage

**As a module:**

```javascript
const { CosmicCommRelay } = require('@polsala/nightly-cosmic-comm-relay');

const relay = new CosmicCommRelay({ distance: 100 }); // Distance in arbitrary units

relay.sendMessage('Greetings from Sector 7G!', (err, receivedMessage) => {
  if (err) {
    console.error('Transmission failed:', err);
  } else {
    console.log('Received:', receivedMessage);
  }
});
```

**As a CLI tool:**

```bash
npx @polsala/nightly-cosmic-comm-relay "Your message here" --distance 50
```

### Options (CLI)

*   `message`: The string message to send.
*   `--distance` (optional): The simulated cosmic distance (default: 100). Higher values mean longer delays.

### How it Works

The `CosmicCommRelay` class simulates a journey through space. The `distance` parameter influences the base delay. Randomness is introduced to simulate "cosmic static" and minor fluctuations in the transmission speed. The `sendMessage` method uses `setTimeout` to mimic the travel time and `Math.random` to add noise.

### Testing

Run the tests using:

```bash
npm test
```
