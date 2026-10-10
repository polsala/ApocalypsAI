## Nightly Cosmic Communication Relay

This whimsical Node.js utility simulates sending and receiving messages across the vast expanse of the cosmos. It's designed to be fun and a little unpredictable, with an optional 'cosmic interference' mode that can garble messages.

### Features

*   **Send Messages**: Transmit messages to a designated 'cosmic destination'.
*   **Receive Messages**: Listen for incoming messages from the void.
*   **Cosmic Interference**: Optionally introduce random errors, delays, or distortions to messages.
*   **Whimsical Output**: Enjoy fun, space-themed console logs.

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

*   `--interference` or `-i`: Enable cosmic interference mode. Messages may be altered.
*   `--delay <ms>`: Set a base delay in milliseconds for message transmission/reception (default: 1000).
*   `--listen`: Only listen for incoming messages.
*   `--send <message>`: Send a specific message and then exit.

**Examples:**

*   Start the relay with default settings:
    ```bash
    node src/main.js
    ```
*   Start the relay with cosmic interference:
    ```bash
    node src/main.js --interference
    ```
*   Send a single message and exit:
    ```bash
    node src/main.js --send "Greetings from Sector 7G!"
    ```
*   Listen for messages with a 500ms delay:
    ```bash
    node src/main.js --listen --delay 500
    ```

### How it Works

The utility uses Node.js's built-in `setTimeout` and `setInterval` to simulate asynchronous communication. The `cosmicInterference` function randomly modifies messages when the `--interference` flag is used.

### Testing

Run the tests using:

```bash
npm test
```
