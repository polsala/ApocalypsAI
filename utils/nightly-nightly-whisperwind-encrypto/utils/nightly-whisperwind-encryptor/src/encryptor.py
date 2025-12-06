import argparse
import sys

def _char_to_int(char):
    """Converts an uppercase alphabetic character to its 0-25 integer value."""
    return ord(char.upper()) - ord('A')

def _int_to_char(integer):
    """Converts a 0-25 integer value back to an uppercase alphabetic character."""
    return chr(integer + ord('A'))

def vigenere_transform(text, key, encrypt_mode=True):
    """Applies Vigenere cipher transformation (encrypt or decrypt) to the text.

    Args:
        text (str): The input text to transform.
        key (str): The passphrase for the cipher. Only alphabetic characters are used.
        encrypt_mode (bool): True for encryption, False for decryption.

    Returns:
        str: The transformed text.

    Raises:
        ValueError: If the key contains no alphabetic characters.
    """
    result = []
    key_upper_alpha = [c for c in key.upper() if 'A' <= c <= 'Z']
    if not key_upper_alpha:
        raise ValueError("Key must contain at least one alphabetic character.")

    key_len = len(key_upper_alpha)
    key_idx = 0

    for char in text:
        if 'A' <= char.upper() <= 'Z':
            p_val = _char_to_int(char)
            k_val = _char_to_int(key_upper_alpha[key_idx % key_len])

            if encrypt_mode:
                c_val = (p_val + k_val) % 26
            else:  # decrypt_mode
                c_val = (p_val - k_val + 26) % 26  # Add 26 to handle negative results correctly

            # Preserve original case
            if char.islower():
                result.append(_int_to_char(c_val).lower())
            else:
                result.append(_int_to_char(c_val))
            key_idx += 1
        else:
            result.append(char)  # Non-alphabetic characters are passed through
    return "".join(result)

def vigenere_encrypt(text, key):
    """Encrypts text using the Vigenere cipher."""
    return vigenere_transform(text, key, encrypt_mode=True)

def vigenere_decrypt(text, key):
    """Decrypts text using the Vigenere cipher."""
    return vigenere_transform(text, key, encrypt_mode=False)

def main():
    """Main function to parse arguments and run the encryptor/decryptor."""
    parser = argparse.ArgumentParser(
        description="Whisperwind Message Encryptor: Obfuscate your messages for the uncertain future."
    )
    parser.add_argument('--mode', choices=['encrypt', 'decrypt'], required=True,
                        help="Operation mode: 'encrypt' to obfuscate, 'decrypt' to reveal.")
    parser.add_argument('--text', required=True,
                        help="The message to process.")
    parser.add_argument('--key', required=True,
                        help="The secret passphrase (alphabetic characters only are used for the key).")
    args = parser.parse_args()

    try:
        if args.mode == 'encrypt':
            result = vigenere_encrypt(args.text, args.key)
            print(f"Whisperwind Encrypted: {result}")
        else:
            result = vigenere_decrypt(args.text, args.key)
            print(f"Whisperwind Decrypted: {result}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
