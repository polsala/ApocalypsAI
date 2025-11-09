# Wasteland Whisperer: Encrypted Message Utility

In the desolate expanse of the post-apocalyptic world, reliable communication is a luxury. The `Wasteland Whisperer` is your trusty companion for sending and receiving messages with a touch of secrecy. This simple command-line tool employs a classic Caesar cipher to encode and decode text, ensuring your vital intel or witty banter remains just between you and your trusted allies.

## Features

*   **Encode Messages**: Shift characters forward to obscure your text.
*   **Decode Messages**: Shift characters backward to reveal hidden meanings.
*   **Simple & Effective**: Uses a well-known substitution cipher, easy to understand and implement.
*   **Self-Contained**: No external dependencies, just pure Python.

## Usage

Navigate to the `utils/wasteland-whisperer` directory and run the `whisperer.py` script.

### Encoding a message

To encode a message, use the `encode` command followed by your message (in quotes if it contains spaces) and the numerical shift value.

```bash
python src/whisperer.py encode "Hello, brave survivor!" 3
# Output: Khoor, eudyh vxuylyru!
```

### Decoding a message

To decode a message, use the `decode` command, the encrypted message, and the *same* numerical shift value used for encoding.

```bash
python src/whisperer.py decode "Khoor, eudyh vxuylyru!" 3
# Output: Hello, brave survivor!
```

### Examples

*   **Encode with shift 5:**
    ```bash
    python src/whisperer.py encode "The secret bunker is at coordinates X-Y-Z." 5
    # Output: Ymj xjhwjy gzspjw nx ny htwwlqnyjxj C-D-E.
    ```

*   **Decode with shift 5:**
    ```bash
    python src/whisperer.py decode "Ymj xjhwjy gzspjw nx ny htwwlqnyjxj C-D-E." 5
    # Output: The secret bunker is at coordinates X-Y-Z.
    ```

*   **Handling non-alphabetic characters:**
    Numbers, symbols, and spaces are preserved as-is.
    ```bash
    python src/whisperer.py encode "Attack at dawn! Code: Alpha-7" 1
    # Output: Buubdl bu ebxo! Dpef: Bmqib-7
    ```
