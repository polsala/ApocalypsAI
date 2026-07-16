# Nightly Cosmic Comm Relay

This utility simulates sending and receiving messages across the vastness of space. It's designed to be whimsical and a bit unpredictable, just like the cosmos itself!

## Features

*   **Send Messages**: Craft a message and send it into the void.
*   **Receive Messages**: Listen for incoming transmissions from distant stars.
*   **Cosmic Interference**: Optionally introduce random 'interference' that can garble messages or create unexpected transmissions.
*   **Cross-Platform**: Runs on any system with Node.js installed.

## Installation

```bash
npm install -g @polsala/nightly-cosmic-comm-relay
```

## Usage

**Sending a message:**

```bash
cosmic-relay send "Greetings, fellow travelers!"
```

**Receiving messages (runs indefinitely until interrupted):

```bash
cosmic-relay receive
```

**Receiving messages with cosmic interference enabled:**

```bash
cosmic-relay receive --interfere
```

## How it Works

The utility uses a simple probabilistic model to simulate message transmission and reception. When interference is enabled, there's a chance messages might be altered or new, unexpected messages might appear.

## Development & Testing

This utility is built with Node.js and uses Jest for testing. All tests are deterministic and run offline using mocks.

To run tests:

```bash
npm install
npm test
```
