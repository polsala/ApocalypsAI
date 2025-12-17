## Nightly Cosmic Comm Relay

This utility simulates a whimsical, yet functional, cosmic communication relay. It allows you to send encrypted messages across vast, imaginary distances, with a touch of randomized signal degradation to keep things interesting.

### Philosophy

In the face of the apocalypse, even communication needs a bit of flair and resilience. This tool embraces the chaos with a playful approach to data transmission.

### Features

*   **End-to-End Encryption**: Messages are encrypted using a simple XOR cipher for basic security.
*   **Simulated Signal Degradation**: Randomly introduces noise and data loss to mimic the challenges of interstellar communication.
*   **Cross-Platform**: Built with Node.js, it runs on any system with Node.js installed.
*   **Whimsical Interface**: Uses fun, space-themed terminology.

### Installation

1.  Clone this repository.
2.  Navigate to the `utils/nightly-cosmic-comm-relay` directory.
3.  Run `npm install` to install dependencies.

### Usage

**Sending a Message:**

```bash
node src/send.js <recipient_id> <your_message>
```

*   `<recipient_id>`: A unique identifier for the recipient (e.g., 'AlphaCentauri_Station_7').
*   `<your_message>`: The message you wish to send.

**Receiving Messages:**

```bash
node src/receive.js <your_id>
```

*   `<your_id>`: Your unique identifier (the same one used by senders to target you).

**Key Management (for demonstration purposes):**

This utility uses a simple, hardcoded key for encryption. In a real-world scenario, you would implement a more robust key exchange mechanism.

### How it Works

*   **Encryption**: Messages are XORed with a repeating key. The key is derived from the recipient's ID and a secret passphrase.
*   **Signal Degradation**: When sending, a random percentage of bits in the message are flipped, and a random number of characters might be dropped to simulate interference.
*   **Storage**: Messages are stored in a simple in-memory array (for demonstration). In a production system, you'd use a database or persistent storage.

### Testing

Run `npm test` in the `utils/nightly-cosmic-comm-relay` directory to execute the automated tests.

### Contributing

Feel free to fork this repository and submit pull requests. Let's make communication more resilient and fun!
