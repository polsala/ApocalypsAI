## Nightly Cosmic Comm Relay

This utility simulates a whimsical communication relay between hypothetical cosmic entities. It allows you to define custom 'dialects' for these entities and send messages through the relay, which then translates them based on the defined dialects.

### Features

*   **Cosmic Entity Simulation**: Create and manage simulated cosmic entities.
*   **Custom Dialects**: Define unique communication styles (e.g., punctuation, word order, common phrases) for each entity.
*   **Message Relaying**: Send messages through the relay, which translates them based on sender and receiver dialects.
*   **Whimsical Output**: Enjoy the playful nature of cosmic communication.

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

Run the main script:

```bash
node src/main.js
```

This will start a demonstration of the Cosmic Comm Relay.

### Defining Dialects

Dialects are defined in the `src/dialects.js` file. Each dialect is an object with properties that modify how messages are sent and received.

**Example Dialect (`nebula_speak`)**:

```javascript
nebula_speak: {
  prefix: "(Whispers from the void) ",
  suffix: " ...across the cosmos.",
  transform: (message) => {
    // Adds a random cosmic-sounding word
    const cosmicWords = ["stardust", "quasars", "galaxies", "void", "ether"];
    const randomWord = cosmicWords[Math.floor(Math.random() * cosmicWords.length)];
    return message.split(' ').join(` ${randomWord} `);
  }
}
```

### How it Works

The `CosmicRelay` class manages entities and their dialects. When a message is sent, it fetches the sender's dialect, applies its transformation, and then fetches the receiver's dialect to apply its prefix and suffix.

### Testing

Run the tests:

```bash
npm test
```

### Contributing

Feel free to add more whimsical dialects or improve the relay logic!
