import argparse
import sys

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEFAULT_KEY = "XPMGTDHLYONZWEQJRUVICSAKFB"

def validate_key(key: str) -> None:
    """Validates if the provided key is a valid 26-character substitution key."""
    if not isinstance(key, str) or len(key) != 26:
        raise ValueError("Key must be a 26-character string.")
    if not key.isupper():
        raise ValueError("Key must contain only uppercase letters.")
    if len(set(key)) != 26:
        raise ValueError("Key must contain 26 unique uppercase letters.")

def encrypt(plaintext: str, key: str = DEFAULT_KEY) -> str:
    """Encrypts a plaintext message using a substitution cipher."""
    validate_key(key)
    mapping = {ALPHABET[i]: key[i] for i in range(26)}
    ciphertext = []
    for char in plaintext.upper():
        if char in mapping:
            ciphertext.append(mapping[char])
        else:
            ciphertext.append(char) # Preserve non-alphabetic characters
    return "".join(ciphertext)

def decrypt(ciphertext: str, key: str = DEFAULT_KEY) -> str:
    """Decrypts a ciphertext message using a substitution cipher."""
    validate_key(key)
    reverse_mapping = {key[i]: ALPHABET[i] for i in range(26)}
    plaintext = []
    for char in ciphertext.upper():
        if char in reverse_mapping:
            plaintext.append(reverse_mapping[char])
        else:
            plaintext.append(char) # Preserve non-alphabetic characters
    return "".join(plaintext)

def main():
    parser = argparse.ArgumentParser(
        description="Whisperwind Cipher: Encrypt or decrypt messages using a substitution cipher."
    )
    parser.add_argument(
        "--encrypt", action="store_true", help="Encrypt the provided text."
    )
    parser.add_argument(
        "--decrypt", action="store_true", help="Decrypt the provided text."
    )
    parser.add_argument(
        "--text", type=str, required=True, help="The message to encrypt or decrypt."
    )
    parser.add_argument(
        "--key",
        type=str,
        default=DEFAULT_KEY,
        help=f"The 26-character substitution key (default: {DEFAULT_KEY})."
    )

    args = parser.parse_args()

    if not (args.encrypt or args.decrypt):
        parser.error("Please specify either --encrypt or --decrypt.")
    if args.encrypt and args.decrypt:
        parser.error("Cannot specify both --encrypt and --decrypt.")

    try:
        if args.encrypt:
            result = encrypt(args.text, args.key)
            print(result)
        elif args.decrypt:
            result = decrypt(args.text, args.key)
            print(result)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
