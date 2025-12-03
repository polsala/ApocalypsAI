# Nightly Scrawl Scrambler

## 📜 Whimsical Purpose

In the desolate quiet of the post-apocalypse, where whispers carry far and trust is a rare commodity, the "Nightly Scrawl Scrambler" emerges as your trusty companion for discreet communication. This utility allows survivors to quickly obfuscate (scramble) and de-obfuscate (unscramble) short, sensitive messages using a simple, yet effective, Caesar cipher. Perfect for passing notes about hidden caches, impending raider patrols, or just sharing a secret recipe for mutated squirrel stew without prying eyes immediately understanding.

It's not military-grade encryption, but it's enough to deter casual snoops and keep your secrets safe from the common wasteland wanderer.

## 🛠️ Practical Utility

This tool provides a command-line interface to:
1.  **Encrypt messages**: Transform plain text into a scrambled form using a specified shift value.
2.  **Decrypt messages**: Revert scrambled text back to its original form using the same shift value.

It's self-contained, requires no network access, and is ideal for environments where complex tools are unavailable or unreliable.

## 🚀 How to Use

### Prerequisites

*   Python 3.6+ (tested with Python 3.11)

### Installation

This utility is self-contained. Simply navigate to its directory:

```bash
cd utils/nightly-scrawl-scrambler/src
```

### Encryption

To encrypt a message, run `scrambler.py` with your message and a numerical shift value:

```bash
python scrambler.py "Meet me at the old water tower tonight." 5
# Expected Output: Encrypted: Rjjy rj fy ymj tqi bfymw ytbjw ytslmj.
```

### Decryption

To decrypt a message, add the `--decrypt` flag along with the scrambled message and the *same* shift value used for encryption:

```bash
python scrambler.py "Rjjy rj fy ymj tqi bfymw ytbjw ytslmj." 5 --decrypt
# Expected Output: Decrypted: Meet me at the old water tower tonight.
```

### Examples

*   **Simple message:**
    ```bash
    python scrambler.py "Hello World" 3
    # Encrypted: Khoor Zruog
    python scrambler.py "Khoor Zruog" 3 --decrypt
    # Decrypted: Hello World
    ```

*   **Message with numbers and symbols (these are ignored):**
    ```bash
    python scrambler.py "Cache at Sector 7, Code: X-Y-Z!" 10
    # Encrypted: Mkmru kd Bumtyb 7, Myhu: H-I-J!
    python scrambler.py "Mkmru kd Bumtyb 7, Myhu: H-I-J!" 10 --decrypt
    # Decrypted: Cache at Sector 7, Code: X-Y-Z!
    ```

## 🧪 Development and Testing

The utility includes a comprehensive test suite to ensure its reliability.

To run tests:

```bash
cd utils/nightly-scrawl-scrambler/tests
python -m unittest test_scrambler.py
```

The tests are deterministic and do not require any external resources or network access.
