## Nightly Cosmic Chatter Translator

This utility provides a whimsical way to encode and decode messages into a simulated 'cosmic chatter' language. Perfect for adding a touch of alien fun to your communications or for generating unique identifiers.

### Installation

```bash
npm install @polsala/nightly-cosmic-chatter-translator
```

### Usage

#### Command Line Interface (CLI)

This utility can be run directly from your terminal.

**Encode:**

```bash
npx @polsala/nightly-cosmic-chatter-translator encode "Hello, fellow traveler!"
```

**Decode:**

```bash
npx @polsala/nightly-cosmic-chatter-translator decode "Zorp glorp, flibble snorf!"
```

#### Programmatic Usage (Node.js)

```javascript
const { encode, decode } = require('@polsala/nightly-cosmic-chatter-translator');

const originalMessage = "Greetings from the void!";
const encodedMessage = encode(originalMessage);
console.log(`Encoded: ${encodedMessage}`); // Example: "Glarp zorp from the vord!"

const decodedMessage = decode(encodedMessage);
console.log(`Decoded: ${decodedMessage}`); // Example: "Greetings from the void!"
```

### How it Works

The translation is based on a simple substitution cipher with a few added 'alien' flair. Vowels are often replaced with 'o' or 'p', and consonants might be doubled or swapped with similar-sounding alien phonemes. The exact mapping is designed to be somewhat arbitrary and fun.

### Contributing

Contributions are welcome! Please refer to the main ApocalypsAI repository for contribution guidelines.
