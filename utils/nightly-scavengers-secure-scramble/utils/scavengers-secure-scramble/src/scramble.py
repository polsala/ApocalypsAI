import argparse

def _normalize_char(char):
    """Converts a character to its uppercase alphabetic value (0-25) or returns None."""
    if 'A' <= char <= 'Z':
        return ord(char) - ord('A')
    if 'a' <= char <= 'z':
        return ord(char) - ord('a')
    return None

def _denormalize_char(value, original_case):
    """Converts an alphabetic value (0-25) back to a character, preserving original case."""
    if original_case == 'upper':
        return chr(ord('A') + value)
    return chr(ord('a') + value)

def vigenere_cipher(text, key, mode='encrypt'):
    """
    Encrypts or decrypts text using the Vigenere cipher.
    Non-alphabetic characters are preserved. Case is preserved for alphabetic characters.
    Key is treated as uppercase alphabetic characters only.
    """
    result = []
    key_idx = 0
    
    # Normalize key to a list of 0-25 values, ignoring non-alphabetic characters
    normalized_key = []
    for k_char in key:
        val = _normalize_char(k_char)
        if val is not None:
            normalized_key.append(val)
    
    if not normalized_key:
        raise ValueError("Key must contain at least one alphabetic character.")

    for char in text:
        char_val = _normalize_char(char)
        
        if char_val is None:
            result.append(char) # Preserve non-alphabetic characters
        else:
            original_case = 'upper' if 'A' <= char <= 'Z' else 'lower'
            
            key_shift = normalized_key[key_idx % len(normalized_key)]
            
            if mode == 'encrypt':
                shifted_val = (char_val + key_shift) % 26
            elif mode == 'decrypt':
                shifted_val = (char_val - key_shift + 26) % 26
            else:
                raise ValueError("Mode must be 'encrypt' or 'decrypt'.")
            
            result.append(_denormalize_char(shifted_val, original_case))
            key_idx += 1 # Only advance key index for alphabetic characters

    return "".join(result)

def main():
    parser = argparse.ArgumentParser(
        description="Scavenger's Secure Scramble: A simple Vigenere cipher for your post-apocalyptic messages."
    )
    parser.add_argument("--text", required=True, help="The text to encrypt or decrypt.")
    parser.add_argument("--key", required=True, help="The secret key for the cipher (alphabetic characters only).")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--encrypt", action="store_true", help="Encrypt the provided text.")
    group.add_argument("--decrypt", action="store_true", help="Decrypt the provided text.")

    args = parser.parse_args()

    try:
        if args.encrypt:
            output = vigenere_cipher(args.text, args.key, mode='encrypt')
            print(f"Encrypted: {output}")
        elif args.decrypt:
            output = vigenere_cipher(args.text, args.key, mode='decrypt')
            print(f"Decrypted: {output}")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
