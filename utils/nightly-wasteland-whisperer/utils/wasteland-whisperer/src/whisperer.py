import sys

def _normalize_char(char):
    """Converts an uppercase alphabetic character to its 0-25 integer representation."""
    if 'A' <= char <= 'Z':
        return ord(char) - ord('A')
    return None

def _denormalize_char(value):
    """Converts a 0-25 integer to its uppercase alphabetic character representation."""
    return chr(value % 26 + ord('A'))

def _vigenere_transform(text, key, encrypt=True):
    """
    Performs Vigenere encryption or decryption.

    Args:
        text (str): The plaintext to encrypt or ciphertext to decrypt.
        key (str): The keyword for the cipher.
        encrypt (bool): True for encryption, False for decryption.

    Returns:
        str: The transformed text.
    """
    if not key:
        raise ValueError("Key cannot be empty.")

    processed_key = [
        _normalize_char(char) for char in key.upper() if 'A' <= char <= 'Z'
    ]
    if not processed_key:
        raise ValueError("Key must contain at least one alphabetic character.")

    transformed_chars = []
    key_index = 0

    for char in text:
        if 'A' <= char.upper() <= 'Z':
            is_lower = char.islower()
            text_val = _normalize_char(char.upper())
            key_val = processed_key[key_index % len(processed_key)]

            if encrypt:
                transformed_val = (text_val + key_val) % 26
            else:
                transformed_val = (text_val - key_val + 26) % 26 # Add 26 to handle negative results

            transformed_char = _denormalize_char(transformed_val)
            if is_lower:
                transformed_char = transformed_char.lower()
            transformed_chars.append(transformed_char)
            key_index += 1
        else:
            transformed_chars.append(char) # Preserve non-alphabetic characters
    return "".join(transformed_chars)

def encode(plaintext, key):
    """Encrypts plaintext using the Vigenere cipher."""
    return _vigenere_transform(plaintext, key, encrypt=True)

def decode(ciphertext, key):
    """Decrypts ciphertext using the Vigenere cipher."""
    return _vigenere_transform(ciphertext, key, encrypt=False)

def main():
    if len(sys.argv) < 4:
        print("Usage: python src/whisperer.py <encode|decode> <message> <key>")
        sys.exit(1)

    command = sys.argv[1].lower()
    message = sys.argv[2]
    key = sys.argv[3]

    try:
        if command == "encode":
            result = encode(message, key)
        elif command == "decode":
            result = decode(message, key)
        else:
            print(f"Error: Unknown command '{command}'. Use 'encode' or 'decode'.")
            sys.exit(1)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
