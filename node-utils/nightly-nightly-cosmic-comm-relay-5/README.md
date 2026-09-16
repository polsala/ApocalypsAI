# Nightly Cosmic Comm Relay

This utility simulates a whimsical cosmic communication relay. It allows you to send encrypted messages across vast, simulated distances, with the added fun of signal degradation that can affect message integrity. It's built with Node.js for cross-platform compatibility and ease of use.

## Philosophy

"Anarchy with discipline" — this tool is designed to be fun, slightly chaotic, and yet reliably functional. It embraces the spirit of exploration and communication, even in the face of cosmic interference.

## Features

*   **End-to-end Encryption**: Uses a simple XOR cipher for message security.
*   **Simulated Cosmic Distance**: Messages take time to travel, adjustable via a `delay` parameter.
*   **Signal Degradation**: Introduces random bit flips to simulate interference, controllable via a `degradationRate`.
*   **Cross-Platform**: Runs on any system with Node.js installed.

## Installation

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

## Usage

### Sending a Message

To send a message, run the `send` command:

```bash
node src/relay.js send --message "Hello from Earth!" --recipient "Proxima Centauri" --key "secretkey" --distance 5 --degradationRate 0.05
```

*   `--message`: The plaintext message to send.
*   `--recipient`: The destination of the message (for display purposes).
*   `--key`: The encryption key (a simple string).
*   `--distance`: The simulated distance in light-years (affects travel time).
*   `--degradationRate`: The probability of a bit flip per character (0.0 to 1.0).

### Receiving a Message

To simulate receiving a message, run the `receive` command. This will process any messages that have "arrived" based on their simulated travel time.

```bash
node src/relay.js receive --key "secretkey"
```

*   `--key`: The encryption key used to decrypt messages.

### Example Workflow

**Terminal 1 (Sender):**
```bash
node src/relay.js send --message "Greetings, fellow travelers!" --recipient "Andromeda Galaxy" --key "stardust" --distance 10 --degradationRate 0.1
```

**Terminal 2 (Receiver):**

Wait for the simulated travel time (based on `--distance`). Then run:

```bash
node src/relay.js receive --key "stardust"
```

## Testing

Run the tests using:

```bash
npm test
```

## Contributing

Feel free to suggest improvements or new features! This is a whimsical project, so creativity is encouraged.
