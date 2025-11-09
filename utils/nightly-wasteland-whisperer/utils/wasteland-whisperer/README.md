# Wasteland Whisperer

A simple, self-contained command-line utility for encoding and decoding messages using a basic Caesar cipher. Perfect for clandestine communications in a world where digital networks have crumbled, and you need to pass notes without prying eyes understanding them.

## Purpose

In the desolate future, trust is a rare commodity, and secure communication is paramount. The Wasteland Whisperer provides a quick and easy way to encrypt short messages with a shared numerical key. It's not military-grade encryption, but it's enough to keep casual eavesdroppers guessing and to ensure your vital intel reaches its intended recipient.

## How to Use

The utility is written in Python and can be run directly from the command line.

### Prerequisites

*   Python 3.x (tested with Python 3.11)

### Running the Utility

Navigate to the `src` directory within the `wasteland-whisperer` folder.

```bash
cd utils/wasteland-whisperer/src
```

#### Encode a Message

To encode a message, provide the `encode` action, your message (in quotes if it contains spaces), and an integer shift key.

```bash
python whisperer.py encode "Meet me at the old water tower" 5
# Expected output: Encoded message: Rjjy rj fy ymj tqi bfymw ytbjw
```

#### Decode a Message

To decode a message, provide the `decode` action, the encrypted message, and the *same* integer shift key used for encoding.

```bash
python whisperer.py decode "Rjjy rj fy ymj tqi bfymw ytbjw" 5
# Expected output: Decoded message: Meet me at the old water tower
```

### Examples

*   **Sharing a rendezvous point:**
    ```bash
    python whisperer.py encode "Rendezvous Point Alpha at Dawn" 7
    # Output: Slughgcrvbh Qvbuk Hswod gb Kbuq
    ```
    Recipient decodes:
    ```bash
    python whisperer.py decode "Slughgcrvbh Qvbuk Hswod gb Kbuq" 7
    # Output: Rendezvous Point Alpha at Dawn
    ```

*   **A quick warning:**
    ```bash
    python whisperer.py encode "Raiders spotted near sector 7!" 13
    # Output: Envqref fcbggru arne frpgbe 7!
    ```

## Development & Testing

The utility is self-contained and includes a test suite.

### Running Tests

Navigate to the `tests` directory and run `unittest`:

```bash
cd utils/wasteland-whisperer/tests
python -m unittest test_whisperer.py
```

All tests are deterministic and run offline, using mocks for `sys.stdout`, `sys.stderr`, and `sys.argv` to simulate command-line interactions without actual I/O or external dependencies.
