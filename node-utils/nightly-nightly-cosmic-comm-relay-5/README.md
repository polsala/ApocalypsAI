## Nightly Cosmic Comm Relay

This utility simulates the chaotic and whimsical nature of intergalactic communication. It takes a message, adds a random 'cosmic delay' (simulating vast distances and unpredictable wormholes), and may occasionally introduce 'cosmic interference' (simulating stellar flares or alien interference) by slightly altering the message.

### Philosophy

In the vast emptiness of space, communication is never straightforward. This tool embraces the unpredictability and charm of sending messages across the cosmos, adding a touch of fun to the process.

### Features

*   **Simulated Cosmic Delay**: Messages experience a variable delay before 'arrival'.
*   **Cosmic Interference**: A chance of minor message corruption or alteration.
*   **Whimsical Output**: Generates fun, space-themed output.

### Usage

1.  **Install Node.js**: Ensure you have Node.js installed on your system.
2.  **Clone the repository**: `git clone https://github.com/polsala/ApocalypsAI.git`
3.  **Navigate to the utility**: `cd ApocalypsAI/utils/nightly-cosmic-comm-relay`
4.  **Run the utility**: `node src/main.js "Your message here"`

**Example**: `node src/main.js "Greetings from Earth!"`

### Configuration (Optional)

*   `--delay-range <min>,<max>`: Adjust the minimum and maximum delay in milliseconds. Defaults to `1000,5000`.
*   `--interference-chance <percentage>`: Set the probability of interference (0-100). Defaults to `20`.

**Example with options**: `node src/main.js "We come in peace" --delay-range 500,2000 --interference-chance 10`

### Testing

Run the tests using:
`npm install`
`npm test`

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.
