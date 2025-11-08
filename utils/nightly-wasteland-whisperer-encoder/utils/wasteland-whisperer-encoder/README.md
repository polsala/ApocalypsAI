# Wasteland Whisperer Encoder

## A Low-Bandwidth Communication Utility for the End Times

In the desolate future, every character counts. The `Wasteland Whisperer Encoder` is a simple, yet effective, utility designed to compress and standardize critical messages for transmission across unreliable, low-bandwidth radio channels. It replaces common post-apocalyptic terms with short, predefined codes, ensuring your vital communications get through with minimal data.

### Features

*   **Dictionary Compression**: Replaces frequently used survival terms (e.g., 'DANGER', 'WATER', 'BASE') with compact, three-letter codes.
*   **Normalization**: Converts messages to uppercase and strips non-alphanumeric characters for consistent encoding.
*   **Bidirectional**: Encode messages for transmission and decode received messages back to their original intent.

### How to Use

This utility provides two main functions: `encode_message` and `decode_message`.

#### Encoding a Message

To prepare a message for transmission, use the `encode_message` function. It will process your input, substitute known terms, and return the compact version.

```python
from src.encoder import encode_message

original_message = "DANGER! Enemy spotted near the WATER source. Proceed with caution to BASE NORTH."
encoded_message = encode_message(original_message)
print(f"Original: {original_message}")
print(f"Encoded: {encoded_message}")
# Expected Encoded: DGR ENY SPOTTED NEAR THE WTR SOURCE PROCEED WITH CAUTION TO BAS NRT
```

#### Decoding a Message

Upon receiving a coded message, use the `decode_message` function to revert the codes back to their original, more readable forms.

```python
from src.encoder import decode_message

received_message = "HLP FRN SGN UKN LOC OVR"
decoded_message = decode_message(received_message)
print(f"Received: {received_message}")
print(f"Decoded: {decoded_message}")
# Expected Decoded: HELP FRIENDLY SIGNAL UNKNOWN LOCATION OVER
```

### Technical Details

The encoder uses a fixed dictionary of common wasteland terms and their corresponding 3-letter codes. Messages are normalized to uppercase and non-alphanumeric characters (except spaces) are removed before substitution. The process is deterministic and reversible, ensuring reliable communication in the harshest environments.
