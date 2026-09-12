## Nightly Cosmic Communication Relay

This utility simulates the unpredictable nature of interstellar communication by introducing artificial delays and packet loss to network requests.

### Philosophy

In the vast expanse of the cosmos, communication is never instantaneous. This tool brings a touch of that cosmic reality to your local development environment, helping you build more resilient applications.

### Features

*   **Configurable Delay**: Set a minimum and maximum delay for network requests.
*   **Configurable Packet Loss**: Define a probability of packets being 'lost' (requests failing).
*   **Cross-Platform**: Runs on any system with Node.js installed.
*   **Whimsical Interface**: Enjoy the theme of space communication.

### Installation

```bash
npm install @polsala/nightly-cosmic-comm-relay
```

### Usage

**As a module:**

```javascript
const { CosmicCommRelay } = require('@polsala/nightly-cosmic-comm-relay');

const relay = new CosmicCommRelay({
  minDelayMs: 500, // Minimum delay in milliseconds
  maxDelayMs: 3000, // Maximum delay in milliseconds
  packetLossRate: 0.15 // 15% chance of packet loss
});

async function sendCosmicMessage(url) {
  try {
    const response = await relay.fetch(url);
    console.log('Cosmic message received:', response.data);
  } catch (error) {
    console.error('Cosmic message lost in transit:', error.message);
  }
}

sendCosmicMessage('https://api.example.com/data');
```

**As a CLI tool (future enhancement - not implemented in this version):**

```bash
# Example (hypothetical):
# cosmic-comm-relay --url https://api.example.com/data --min-delay 1000 --max-delay 5000 --loss 0.2
```

### Configuration Options

*   `minDelayMs` (number): The minimum delay in milliseconds to apply to requests. Defaults to `100`.
*   `maxDelayMs` (number): The maximum delay in milliseconds to apply to requests. Defaults to `1000`.
*   `packetLossRate` (number): The probability (0.0 to 1.0) of a request failing due to packet loss. Defaults to `0.05`.

### Testing

Run the tests using:

```bash
npm test
```

### Contributing

Feel free to send a PR with new features or improvements!
