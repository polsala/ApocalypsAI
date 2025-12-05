# Wasteland Whisperer

"Whisper your secrets across the desolate plains, safe from prying ears!"

The Wasteland Whisperer is a simple command-line utility designed for encoding and decoding messages using a basic substitution cipher (a Caesar cipher variant). It's perfect for sharing quick, obfuscated notes with your fellow survivors without needing complex encryption.

## Features

*   **Simple Encoding/Decoding**: Easily transform plain text into 'whispers' and back.
*   **Adjustable Scramble Factor**: Control the complexity of your cipher with a numerical key.
*   **Offline & Self-Contained**: No internet required, just a Python interpreter.

## How to Use

### Prerequisites

*   Python 3.6+ (tested with 3.11)

### Running the Utility

Navigate to the `src` directory and run `whisperer.py` with the desired mode, text, and scramble factor.

```bash
# Encode a message
python src/whisperer.py --mode encode --text "Hello, survivor!" --scramble-factor 3
# Expected Output: Khoor, vxuylyru!

# Decode a message
python src/whisperer.py --mode decode --text "Khoor, vxuylyru!" --scramble-factor 3
# Expected Output: Hello, survivor!

# Example with a different scramble factor and longer text
python src/whisperer.py --mode encode --text "The quick brown fox jumps over the lazy dog." --scramble-factor 13
# Expected Output: Gur dhvpx oebja sbk whzcf bire gur ynml qbt.

python src/whisperer.py --mode decode --text "Gur dhvpx oebja sbk whzcf bire gur ynml qbt." --scramble-factor 13
# Expected Output: The quick brown fox jumps over the lazy dog.
```

### Arguments

*   `--mode` (required): `encode` or `decode`.
*   `--text` (required): The message to process.
*   `--scramble-factor` (required): An integer representing the shift amount for the cipher. Can be positive or negative.

## Example

```bash
# Encode a message for your scavenging team
python src/whisperer.py --mode encode --text "Meet me at the old water tower tonight." --scramble-factor 7
# Output: Tlly tl ha aol vsz dhaly avdly avupnoa.

# Decode a message received from a comrade
python src/whisperer.py --mode decode --text "Tlly tl ha aol vsz dhaly avdly avupnoa." --scramble-factor 7
# Output: Meet me at the old water tower tonight.
```
