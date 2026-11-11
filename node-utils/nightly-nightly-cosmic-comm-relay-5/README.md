## Nightly Cosmic Comm Relay

This utility simulates a whimsical cosmic radio frequency to encode and decode messages. Imagine sending secret transmissions across the galaxy with a touch of stardust!

### Philosophy

Embrace the unknown, communicate with flair, and always leave a little sparkle in your transmissions.

### Usage

1.  **Installation**:
    ```bash
    npm install
    ```

2.  **Encoding a message**:
    ```bash
    node src/main.js encode "Hello from Earth!"
    ```

3.  **Decoding a message**:
    ```bash
    node src/main.js decode <encoded_message>
    ```

    *Replace `<encoded_message>` with the output from the `encode` command.*

### How it Works

The utility assigns a unique, arbitrary "cosmic frequency" (a number between 1000 and 9999) to each character. The encoding process involves summing the ASCII values of the message characters and then adding the assigned "cosmic frequency" for each character. Decoding reverses this process.

### Contributing

Feel free to suggest new cosmic characters or more elaborate encoding schemes! Just open an issue or a PR.
