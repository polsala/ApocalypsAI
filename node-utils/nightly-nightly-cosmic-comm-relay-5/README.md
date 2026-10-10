## Nightly Cosmic Comm Relay

This utility simulates the whimsical challenges of communicating across vast cosmic distances. It introduces random delays and message corruption to mimic the unpredictable nature of interstellar communication.

### Features

*   **Simulated Delays**: Messages are delayed by a random amount, representing light-speed travel.
*   **Cosmic Corruption**: Messages have a chance of being slightly altered, adding a touch of the unknown.
*   **Configurable Parameters**: Adjust delay ranges and corruption probability.

### Installation

```bash
npm install
```

### Usage

Run the utility from your terminal:

```bash
node src/main.js
```

**Example Output:**

```
Sending message: "Greetings from Sector 7G!"
Received message: "Gretings from Sector 7G!" after 1500ms delay.

Sending message: "Report status: All clear."
Received message: "Report status: All clear." after 3200ms delay.

Sending message: "Encountered anomaly in Nebula X."
Received message: "Encountered anomly in Nebula X." after 2800ms delay.
```

### Configuration

You can modify the following constants in `src/main.js`:

*   `MIN_DELAY_MS`: Minimum communication delay in milliseconds.
*   `MAX_DELAY_MS`: Maximum communication delay in milliseconds.
*   `CORRUPTION_CHANCE`: Probability (0.0 to 1.0) of a message being corrupted.
*   `MESSAGES_TO_SEND`: Number of messages to simulate.

### Testing

Run the tests using:

```bash
npm test
```
