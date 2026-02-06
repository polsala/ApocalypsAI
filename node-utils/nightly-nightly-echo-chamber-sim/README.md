# Nightly Echo Chamber Simulator

The Nightly Echo Chamber Simulator is a whimsical-yet-useful utility designed to illustrate how information can transform and distort as it passes through a series of "nodes" in a communication chain, much like a post-apocalyptic whisper network. It helps you visualize the potential for misinterpretation, simplification, or amplification of a message over time.

## Features

-   Simulate message propagation over a configurable number of "hops".
-   Apply a deterministic truncation factor at each hop, mimicking information loss or summarization.
-   Apply a set of predefined word replacements to simulate misinterpretation or semantic shifts.
-   Command-line interface for easy use.

## Installation

1.  **Navigate to the utility directory:**
    ```bash
    cd node-utils/nightly-echo-chamber-sim
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```

## Usage

Run the simulator from the command line:

```bash
node src/index.js --message "The ancient scrolls speak of a hidden bunker beneath the old city ruins, filled with pre-collapse tech and sustenance for a thousand years." --hops 3 --truncationFactor 0.8 --replacements '{"scrolls":"papers", "bunker":"shelter", "tech":"gadgets", "sustenance":"food"}'
```

### Arguments

-   `--message <string>`: The initial message to propagate through the echo chamber. (Required)
-   `--hops <number>`: The number of times the message will be processed. Each hop represents a new node in the network. (Default: `5`)
-   `--truncationFactor <number>`: A decimal between 0 and 1. At each hop, the message's word count will be multiplied by this factor. E.g., `0.8` means 20% of words are removed. (Default: `0.9`)
-   `--replacements <json_string>`: A JSON string representing a map of words to replace. E.g., `'{"old":"ancient", "city":"town"}'`. (Default: `{}`)

## Examples

### Basic Simulation
```bash
node src/index.js --message "We need to find the lost artifact before the temporal rifts destabilize completely." --hops 2 --truncationFactor 0.7
```

### With Word Replacements
```bash
node src/index.js --message "The void whispers are growing louder, signaling an imminent cosmic alignment." --hops 3 --truncationFactor 0.9 --replacements '{"void":"empty", "whispers":"sounds", "cosmic":"star", "alignment":"event"}'
```

## Development

### Running Tests

```bash
npm test
```
