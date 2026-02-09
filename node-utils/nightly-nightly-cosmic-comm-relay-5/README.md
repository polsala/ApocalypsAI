## Nightly Cosmic Comm Relay

This utility simulates a whimsical cosmic radio frequency to encode and decode messages. Imagine you're an interstellar traveler needing to send a secret message across the void using only the hum of the universe. This tool helps you do just that!

### Philosophy

Embrace the absurdity of the cosmos while maintaining a functional communication channel. This tool is designed to be fun, slightly mysterious, and surprisingly useful for simple, obfuscated messaging.

### Installation

```bash
npm install
```

### Usage

**Encoding a message:**

```bash
node src/main.js encode "Hello, fellow traveler!"
```

This will output a "cosmic frequency" string.

**Decoding a message:**

```bash
node src/main.js decode "<output_from_encode>"
```

This will output the original message.

### How it Works

The tool uses a simple substitution cipher based on prime numbers and a pseudo-random sequence derived from the message length. Each character is mapped to a unique "frequency" pattern.

### Testing

Run the tests using:

```bash
npm test
```
