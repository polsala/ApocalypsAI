## Nightly Cosmic Comm Relay

This utility allows you to send and receive secret messages across the cosmos using a whimsical encoding scheme based on stellar coordinates and a dash of intergalactic flair.

### Philosophy

In the vast expanse of the universe, communication is key. This tool embraces the idea that even the most dire situations can be navigated with a bit of creativity and a well-placed star chart. It's designed to be fun, functional, and a little bit silly.

### Installation

1. Clone this repository.
2. Navigate to the `utils/nightly-cosmic-comm-relay` directory.
3. Run `npm install`.

### Usage

**Encoding a message:**

```bash
node src/main.js encode "Hello, fellow traveler!" "Sirius B" "Alpha Centauri A"
```

This will output a string representing the encoded message, using the provided star names as anchors.

**Decoding a message:**

```bash
node src/main.js decode "<encoded_message_string>" "Sirius B" "Alpha Centauri A"
```

Replace `<encoded_message_string>` with the output from the `encode` command.

### How it Works

The utility takes a plaintext message and two star names. It converts each character of the message into a numerical representation and then maps these numbers to a simplified coordinate system derived from the positions of the two provided stars. The decoding process reverses this mapping.

### Testing

To run the tests, navigate to the `utils/nightly-cosmic-comm-relay` directory and run:

```bash
npm test
```

### Contributing

Feel free to suggest new celestial bodies or more outlandish encoding methods! Open an issue or a pull request.
