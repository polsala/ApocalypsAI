## Nightly Cosmic Comm Relay

This utility simulates the whimsical challenges of interstellar communication. It takes a message and a 'distance' parameter, then applies a simulated delay and a chance of 'cosmic interference' (message corruption) before returning the potentially altered message.

### Philosophy

In the vastness of space, communication is never straightforward. This tool embraces the chaos and unpredictability of sending messages across the cosmos, adding a touch of fun to the concept of network latency and packet loss.

### Usage

1.  **Install dependencies:**
    ```bash
    npm install
    ```

2.  **Run the utility:**
    ```bash
    node src/main.js "Hello from Earth!" 100
    ```

    *   The first argument is the message string.
    *   The second argument is the simulated distance in 'light-years' (determines delay and corruption chance).

### How it Works

*   **Delay Simulation:** The delay is proportional to the distance, mimicking light-speed travel.
*   **Cosmic Interference:** A random chance of characters in the message being altered, replaced with random characters, or deleted entirely, based on the distance.

### Testing

Run the tests using:

```bash
npm test
```

This will execute the deterministic tests that mock the random number generator to ensure consistent results.
