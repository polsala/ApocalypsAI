## Nightly Cosmic Comm Relay

This utility simulates a whimsical intergalactic communication relay. It allows you to send messages with customizable delays, introduce "cosmic static" (random character corruption), and simulate signal degradation. Perfect for adding a touch of sci-fi charm to your development environment or for creative projects.

### Features

*   **Customizable Delays**: Simulate light-speed lag or wormhole transit times.
*   **Cosmic Static**: Introduce random character corruption to messages.
*   **Signal Degradation**: Simulate signal loss over distance.
*   **Whimsical Tone**: Messages are framed with fun, space-themed prefixes and suffixes.
*   **Cross-Platform**: Runs anywhere Node.js is installed.

### Installation

1.  Clone this repository.
2.  Navigate to the `utils/nightly-cosmic-comm-relay` directory.
3.  Run `npm install` to install dependencies.

### Usage

Run the utility from your terminal:

```bash
node src/main.js "Hello from Earth!"
```

**Options**:

*   `--delay <ms>`: Set a fixed delay in milliseconds for message transmission (default: 500).
*   `--static-chance <0-1>`: Probability of a character being corrupted by static (default: 0.05).
*   `--degradation <0-1>`: Probability of the entire message being partially degraded (default: 0.1).
*   `--prefix <string>`: Custom prefix for messages (default: "[Galactic Dispatch] ").
*   `--suffix <string>`: Custom suffix for messages (default: " [End Transmission]").

**Example with options**:

```bash
node src/main.js "We have detected a new anomaly!" --delay 2000 --static-chance 0.1 --degradation 0.2
```

### How it Works

The utility takes a message as input, applies optional static and degradation effects, and then simulates transmission with a delay. The output is a "received" message, potentially altered by the simulated cosmic phenomena.

### Testing

Run the tests using:

```bash
npm test
```

### License

This project is licensed under the MIT License.
