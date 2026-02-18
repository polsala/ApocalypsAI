## Nightly Cosmic Comm Relay

Embark on a journey through the cosmos with the Nightly Cosmic Comm Relay! This whimsical Node.js utility allows you to send and receive encrypted messages across simulated vast distances. Imagine sending a secret message to a friend on a distant nebula, or receiving a cryptic transmission from an unknown entity.

### Lore

In the year 2742, the Great Cosmic Silence descended. Interstellar communication became a relic of the past. But then, whispers emerged of the 'Cosmic Comm Relay' – a decentralized network of ancient, repurposed star-faring devices capable of bending spacetime just enough to transmit encrypted data. This utility is your personal gateway to that network.

### Features

*   **End-to-End Encryption**: Messages are encrypted using a simple XOR cipher for a touch of retro-futuristic security.
*   **Simulated Cosmic Delay**: Messages experience a simulated delay based on a configurable 'distance' parameter, adding to the cosmic feel.
*   **Cross-Platform**: Runs on any system with Node.js installed.
*   **Whimsical Interface**: Command-line prompts designed to evoke a sense of space exploration.

### Installation

1.  **Prerequisites**: Ensure you have Node.js and npm installed.
2.  **Clone the repository**: `git clone https://github.com/polsala/ApocalypsAI.git`
3.  **Navigate to the utility**: `cd ApocalypsAI/utils/nightly-cosmic-comm-relay`
4.  **Install dependencies**: `npm install`

### Usage

Run the utility from your terminal:

```bash
node src/main.js
```

The utility will guide you through the following steps:

1.  **Choose Mode**: Select 'send' to transmit a message or 'receive' to listen for incoming transmissions.
2.  **Enter Key**: Provide a secret key for encryption/decryption. Keep this secret!
3.  **Enter Message (for sending)**: Type your message. It will be encrypted and sent.
4.  **Enter Distance (for sending)**: A number representing simulated cosmic distance (e.g., 1000 for a short hop, 1000000 for a long haul). This affects the delay.
5.  **Listen (for receiving)**: The utility will simulate listening for messages. If a message is 'received' (based on mock data), it will be decrypted and displayed.

### Example (Sending)

```
Welcome to the Cosmic Comm Relay!
Choose mode (send/receive): send
Enter your secret key: mySuperSecretKey123
Enter your message: Greetings from Earth!
Enter simulated cosmic distance (e.g., 10000): 50000

Transmitting message...
Message encrypted and sent across the void!
Simulated travel time: 5 seconds.
Transmission complete.
```

### Example (Receiving)

```
Welcome to the Cosmic Comm Relay!
Choose mode (send/receive): receive
Enter your secret key: mySuperSecretKey123

Listening for transmissions...
(Waits for simulated incoming message)

Incoming transmission detected!
Simulated travel time: 3 seconds.
Message decrypted: Greetings from Earth!
```

### Development & Testing

This utility includes unit tests that mock external dependencies and simulate message transmission. To run the tests:

```bash
npm test
```

### Contributing

Feel free to fork this repository and contribute your own cosmic communication protocols or add more whimsical features! Just ensure your changes adhere to the ApocalypsAI philosophy of isolation and testability.
