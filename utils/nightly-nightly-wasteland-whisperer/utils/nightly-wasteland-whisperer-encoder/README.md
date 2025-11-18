# Wasteland Whisperer Encoder

## "Whisper your secrets across the desolate plains."

This utility provides a simple, fixed-key substitution cipher for encoding and decoding short messages. In a world where communication is vital but trust is scarce, the Wasteland Whisperer Encoder offers a basic layer of discretion for your transmissions.

It's not meant for military-grade encryption, but rather for quick, casual obfuscation to deter casual eavesdroppers or to add a touch of mystery to your communiques.

### Features

*   **Simple Substitution**: Uses a fixed, pre-defined substitution map for consistency.
*   **Case-Insensitive**: Handles both uppercase and lowercase letters, preserving case in output.
*   **Numbers Supported**: Encodes/decodes digits 0-9.
*   **Punctuation & Spaces**: Preserves all other characters as-is.

### Usage

To encode a message:

```bash
python src/encoder.py encode "Hello, survivor! Meet me at the old bridge at 0800."
```

Example output:

```
Itllg, luvxixgx! Dttt dt xt zht glw wxiwht xt 5355.
```

To decode a message:

```bash
python src/encoder.py decode "Itllg, luvxixgx! Dttt dt xt zht glw wxiwht xt 5355."
```

Example output:

```
Hello, survivor! Meet me at the old bridge at 0800.
```

### Running Tests

Ensure you have `pytest` installed (`pip install pytest`).

```bash
pytest tests/test_encoder.py
```
