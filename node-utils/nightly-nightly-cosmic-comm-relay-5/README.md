## Nightly Cosmic Comm Relay

This utility simulates the transmission of intergalactic messages, complete with whimsical delays and the occasional cosmic interference. It's designed to be a fun, standalone Node.js application for testing communication resilience in a playful, apocalyptical context.

### Features

*   **Simulated Message Transmission**: Send messages across simulated vast distances.
*   **Customizable Delays**: Introduce variable delays to mimic light-speed limitations or wormhole instability.
*   **Cosmic Interference**: Simulate message corruption or loss with a configurable error rate.
*   **Whimsical Output**: Enjoy fun, space-themed log messages.

### Installation

1.  Clone this repository.
2.  Navigate to the `utils/nightly-cosmic-comm-relay` directory.
3.  Run `npm install` to install dependencies.

### Usage

Run the utility from your terminal:

```bash
node src/main.js "Hello, distant star!" --delay 500 --error-rate 0.1
```

**Arguments**:

*   `message` (required): The message to send.
*   `--delay` (optional): The base delay in milliseconds (default: 1000).
*   `--error-rate` (optional): The probability of a message being corrupted or lost (0.0 to 1.0, default: 0.05).

### Examples

**Basic transmission**:

```bash
node src/main.js "Greetings from Sector 7G."
```

**Slower transmission with higher error rate**:

```bash
node src/main.js "May your shields be strong." --delay 2000 --error-rate 0.2
```

### Testing

Run the tests using:

```bash
npm test
```
