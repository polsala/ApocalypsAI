# nightly-void-whistle

A Dockerized utility for simulating interdimensional message transmission with echo verification.

## Features

- Sends a message into the void (simulated)
- Waits for an echo (simulated response)
- Verifies integrity of the echo
- Fun and educational containerized tool

## Usage

```bash
# Build the container
docker build -t void-whistle .

# Send a message into the void
docker run --rm void-whistle transmit "Hello from the other side!"

# Example output:
# [TRANSMIT] Sending: Hello from the other side!
# [ECHO] Received: !edis ot rehto eht morf olleH
# [VERIFY] Echo verified: true
```

## Testing

Run the test suite with:

```bash
docker run --rm void-whistle test
```
