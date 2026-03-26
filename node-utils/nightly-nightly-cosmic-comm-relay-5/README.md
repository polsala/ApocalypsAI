## Nightly Cosmic Comm Relay

This utility simulates a whimsical cosmic communication relay. It allows you to send messages across the vastness of space, with a chance of encountering cosmic anomalies that might alter or delay your transmissions. It's built with Node.js for cross-platform compatibility and includes deterministic tests.

### Features

*   **Send Messages**: Transmit messages to a simulated cosmic destination.
*   **Receive Messages**: Listen for incoming messages.
*   **Cosmic Anomalies**: Randomly occurring events that can affect message delivery (e.g., signal degradation, temporal shifts).
*   **Error Handling**: Gracefully handles simulated transmission failures.
*   **Cross-Platform**: Runs on any system with Node.js installed.

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```
2.  Navigate to the utility directory:
    ```bash
    cd utils/nightly-cosmic-comm-relay
    ```
3.  Install dependencies:
    ```bash
    npm install
    ```

### Usage

Run the relay from your terminal:

```bash
node src/main.js
```

The utility will start, and you can interact with it by typing messages in the console. Press `Ctrl+C` to exit.

### How it Works

The relay uses `setTimeout` and `Math.random()` to simulate network latency and cosmic events. Messages are processed asynchronously, and simulated errors are thrown and caught to demonstrate robust handling.

### Testing

To run the included tests:

```bash
npm test
```

### Contributing

Feel free to contribute to the cosmic communication network! Open an issue or a pull request.
