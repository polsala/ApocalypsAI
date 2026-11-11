## Nightly Cosmic Comm Relay

This whimsical Node.js utility simulates sending and receiving messages across the vast expanse of the cosmos. It's designed to be fun and educational, demonstrating basic asynchronous operations and optional signal degradation.

### Features

*   **Send Messages**: Transmit messages to distant cosmic entities.
*   **Receive Messages**: Listen for incoming transmissions.
*   **Signal Degradation**: Optionally simulate signal noise and data loss during transmission.
*   **Whimsical Flavor**: Messages and status updates are infused with a cosmic, slightly absurd tone.

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

Run the utility from your terminal:

```bash
node src/main.js
```

**Options:**

*   `--degrade <percentage>`: Simulate signal degradation. For example, `--degrade 20` will introduce a 20% chance of message corruption or loss.

**Example:**

```bash
node src/main.js --degrade 15
```

This will start the relay with a 15% chance of signal degradation.

### How it Works

The utility uses `setTimeout` to simulate the vast distances and time delays involved in cosmic communication. The `degradeSignal` function introduces randomness to simulate signal interference.

### Testing

To run the automated tests:

```bash
npm test
```
