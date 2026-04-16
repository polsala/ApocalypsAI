# Nightly Cosmic Comm Relay

A whimsical Node.js utility that simulates a cosmic radio frequency to encode and decode messages. Perfect for sending secret transmissions across the galaxy (or just your local network).

## Features

*   **Whimsical Encoding**: Messages are transformed into a series of "cosmic pulses" (numbers) based on a simple, yet fun, algorithm.
*   **Decoding**: Reconstructs original messages from their cosmic pulse sequences.
*   **Cross-Platform**: Runs on any system with Node.js installed.
*   **Self-Contained**: No external dependencies beyond Node.js.

## Installation

No installation required. Simply run the script using Node.js.

## Usage

Run the script from your terminal:

```bash
node src/main.js <encode|decode> <message_or_pulses>
```

**Examples**:

**Encoding a message**:

```bash
node src/main.js encode "Greetings, Earthlings!"
```

Output might look like:

```
Cosmic Pulses: 101,114,103,114,101,101,116,105,110,103,115,32,69,97,114,116,104,108,105,110,103,115,33
```

**Decoding cosmic pulses**:

```bash
node src/main.js decode "101,114,103,114,101,101,116,105,110,103,115,32,69,97,114,116,104,108,105,110,103,115,33"
```

Output might look like:

```
Decoded Message: Greetings, Earthlings!
```

## How it Works (The Whimsy)

Each character in the message is converted to its ASCII (Unicode) code point. These code points are then treated as "frequencies" and slightly modulated by a pseudo-random sequence derived from the message length and a fixed "cosmic constant". This modulation adds a touch of unpredictability, mimicking the vastness of space.

Decoding reverses this process, using the same cosmic constant and message length to reconstruct the original ASCII values and then the characters.

## Testing

Run the tests using Node.js:

```bash
node tests/test_main.js
```
