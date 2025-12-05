import argparse
import os

def caesar_cipher(text, shift, mode='encrypt'):
    """
    Applies a Caesar cipher to the given text.

    Args:
        text (str): The input string to encrypt or decrypt.
        shift (int): The number of positions to shift each letter.
        mode (str): 'encrypt' to shift forward, 'decrypt' to shift backward.

    Returns:
        str: The processed string.
    """
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            shifted_char = chr((ord(char) - start + shift * (1 if mode == 'encrypt' else -1)) % 26 + start)
            result.append(shifted_char)
        elif 'A' <= char <= 'Z':
            start = ord('A')
            shifted_char = chr((ord(char) - start + shift * (1 if mode == 'encrypt' else -1)) % 26 + start)
            result.append(shifted_char)
        else:
            result.append(char) # Non-alphabetic characters remain unchanged
    return "".join(result)

def encrypt_file(filepath, shift):
    """
    Encrypts the content of a file using the Caesar cipher and overwrites the file.

    Args:
        filepath (str): The path to the file to encrypt.
        shift (int): The Caesar cipher shift key.

    Returns:
        str: The encrypted content.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    encrypted_content = caesar_cipher(content, shift, 'encrypt')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(encrypted_content)
    return encrypted_content

def decrypt_file(filepath, shift):
    """
    Decrypts the content of a file using the Caesar cipher and overwrites the file.

    Args:
        filepath (str): The path to the file to decrypt.
        shift (int): The Caesar cipher shift key.

    Returns:
        str: The decrypted content.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    decrypted_content = caesar_cipher(content, shift, 'decrypt')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(decrypted_content)
    return decrypted_content

def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt text files using a Caesar cipher.")
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Operation mode: 'encrypt' or 'decrypt'.")
    parser.add_argument("filepath", help="Path to the text file.")
    parser.add_argument("shift", type=int, help="The Caesar cipher shift key (an integer).")

    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File not found at '{args.filepath}'")
        exit(1)

    if args.mode == "encrypt":
        encrypt_file(args.filepath, args.shift)
        print(f"File '{args.filepath}' encrypted with shift {args.shift}.")
    else:
        decrypt_file(args.filepath, args.shift)
        print(f"File '{args.filepath}' decrypted with shift {args.shift}.")

if __name__ == "__main__":
    main()
