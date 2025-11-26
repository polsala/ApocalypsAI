# Nightly Chronicle Cryptographer

## 📜 Description
In the fractured remnants of civilization, secrets are currency. The `Nightly Chronicle Cryptographer` is a whimsical yet practical utility designed to help survivors encrypt and decrypt their precious text-based chronicles, journals, or manifestos using a simple, shareable Caesar cipher. It's not for thwarting advanced digital spies, but perfect for keeping your notes safe from curious scavengers or rival factions who haven't yet mastered the art of 'shift-decoding'.

## ✨ Features
- **Encrypt Text Files**: Shift letters forward by a specified key.
- **Decrypt Text Files**: Shift letters backward to reveal the original message.
- **Simple & Self-Contained**: Written in Python, requires no external dependencies beyond the standard library.
- **CLI-Driven**: Easy to integrate into scripts or run directly from the command line.

## 🛠️ How to Use

### Prerequisites
- Python 3.x (tested with Python 3.11)

### Running the Utility
Navigate to the `src` directory within the utility's folder and run the `cryptographer.py` script.

```bash
python utils/nightly-chronicle-cryptographer/src/cryptographer.py <mode> <filepath> <shift>
```

- `<mode>`: `encrypt` or `decrypt`
- `<filepath>`: The path to the text file you wish to process.
- `<shift>`: An integer representing the Caesar cipher shift key (e.g., `3` for a 3-letter shift).

**Note**: The utility modifies the file in place. It's recommended to back up important files before encrypting/decrypting.

### Examples

1.  **Encrypting a file named `secret_plans.txt` with a shift of `3`:**
    ```bash
    echo "Attack at dawn!" > secret_plans.txt
    python utils/nightly-chronicle-cryptographer/src/cryptographer.py encrypt secret_plans.txt 3
    cat secret_plans.txt # Output: "Dwwdfn dw gdzq!"
    ```

2.  **Decrypting the same file:**
    ```bash
    python utils/nightly-chronicle-cryptographer/src/cryptographer.py decrypt secret_plans.txt 3
    cat secret_plans.txt # Output: "Attack at dawn!"
    ```

3.  **Encrypting a file with mixed characters:**
    ```bash
    echo "Code: Alpha-123. Rendezvous at Sector 7." > mission.txt
    python utils/nightly-chronicle-cryptographer/src/cryptographer.py encrypt mission.txt 5
    cat mission.txt # Output: "Hvij: Fqshf-123. Sjsijatzt fw Sjhyzs 7."
    ```

## ⚠️ Limitations
- This utility uses a simple Caesar cipher, which is **not suitable for strong cryptographic security**. It's easily breakable with frequency analysis or brute force. Use it for light obfuscation or fun, not for protecting highly sensitive information.
- Only alphabetic characters (A-Z, a-z) are shifted. Numbers, symbols, and spaces remain unchanged.
- The utility modifies files in place. Always ensure you have backups if the content is critical.
