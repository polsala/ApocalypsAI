import string

def _normalize_key(key):
    """Normalizes the key to contain only uppercase alphabetic characters."""
    return ''.join(filter(str.isalpha, key)).upper()

def _vigenere_cipher(text, key, encrypt_mode=True):
    """
    Performs Vigenere encryption or decryption.
    Non-alphabetic characters are ignored. Case is preserved for alphabetic characters.
    """
    normalized_key = _normalize_key(key)
    if not normalized_key:
        raise ValueError("Key must contain at least one alphabetic character.")

    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            key_char = normalized_key[key_index % len(normalized_key)]
            key_shift = ord(key_char) - ord('A')

            if char.isupper():
                start_char = 'A'
            else:
                start_char = 'a'

            char_offset = ord(char) - ord(start_char)

            if encrypt_mode:
                new_offset = (char_offset + key_shift) % 26
            else:
                new_offset = (char_offset - key_shift + 26) % 26 # Add 26 to handle negative results

            result.append(chr(ord(start_char) + new_offset))
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

def encrypt(plaintext: str, key: str) -> str:
    """Encrypts a plaintext message using the Vigenere cipher."""
    return _vigenere_cipher(plaintext, key, encrypt_mode=True)

def decrypt(ciphertext: str, key: str) -> str:
    """Decrypts a ciphertext message using the Vigenere cipher."""
    return _vigenere_cipher(ciphertext, key, encrypt_mode=False)

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer: Encrypt or decrypt messages for post-apocalyptic broadcasts."
    )
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Operation mode: 'encrypt' or 'decrypt'.")
    parser.add_argument("message", help="The message to process.")
    parser.add_argument("key", help="The secret key for encryption/decryption (alphabetic characters only).")

    args = parser.parse_args()

    try:
        if args.mode == "encrypt":
            output = encrypt(args.message, args.key)
            print(f"Encrypted message: {output}")
        else:
            output = decrypt(args.message, args.key)
            print(f"Decrypted message: {output}")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
