# Wasteland Whisperer

## ApocalypsAI Morse Encoder/Decoder

In the desolate future, reliable communication is paramount. The `Wasteland Whisperer` is a simple, yet robust utility designed to encode and decode critical messages using a custom "ApocalypsAI Morse" scheme. This scheme prioritizes clarity and resilience over speed, making it ideal for low-bandwidth, noisy, or otherwise degraded communication channels.

Whether you're sending a distress signal across the irradiated plains or coordinating a scavenging run, the Whisperer ensures your message gets through, one dot and dash at a time.

## Features

*   **ApocalypsAI Morse Encoding**: Converts plain text into a sequence of `.` (dot), `_` (dash), and `|` (space separator) symbols.
*   **Decoding**: Reverts ApocalypsAI Morse back to plain text.
*   **Robustness**: Uses a limited symbol set, making it easier to transmit and interpret even with interference.
*   **CLI Interface**: Easy to use from the command line.

## ApocalypsAI Morse Character Map

The encoding uses a modified International Morse Code mapping for alphanumeric characters and common punctuation.
*   ` ` (space) is encoded as a single `|` character.
*   Unsupported characters are encoded as `~` (tilde) and decoded back to `?`.

## Usage

### Encoding a Message

```bash
python src/whisperer.py encode "HELLO APOCALYPSAI"
```

**Output Example:**
```
.... . ._.. ._.. ___ | ._ .___. ___ _._. ._ ._.. _.__ ._.._ ... ._ ._..
```

### Decoding a Message

```bash
python src/whisperer.py decode ".... . ._.. ._.. ___ | ._ .___. ___ _._. ._ ._.. _.__ ._.._ ... ._ ._.."
```

**Output Example:**
```
HELLO APOCALYPSAI
```

### Help

```bash
python src/whisperer.py --help
```

## Installation

This utility is self-contained and requires Python 3.6+. No external dependencies are needed.

1.  Navigate to the `utils/wasteland-whisperer/` directory.
2.  Run the `whisperer.py` script directly.

## Development

Contributions are welcome! If you want to expand the character set, improve error handling, or add new encoding schemes (e.g., a "Scavenger's Cipher"), feel free to open a PR.
