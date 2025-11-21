import argparse

def caesar_cipher(text: str, key: int, mode: str) -> str:
    """
    Applies a Caesar cipher to the given text.

    Args:
        text (str): The input string to encrypt or decrypt.
        key (int): The shift key (integer).
        mode (str): 'encrypt' or 'decrypt'.

    Returns:
        str: The processed string.
    """
    result = []
    # Adjust key for decryption
    if mode == 'decrypt':
        key = -key

    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            shifted_char = chr((ord(char) - start + key) % 26 + start)
            result.append(shifted_char)
        elif 'A' <= char <= 'Z':
            start = ord('A')
            shifted_char = chr((ord(char) - start + key) % 26 + start)
            result.append(shifted_char)
        else:
            result.append(char) # Keep non-alphabetic characters as they are
    return "".join(result)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer Cipher: Encrypt or decrypt messages using a Caesar cipher."
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["encrypt", "decrypt"],
        required=True,
        help="Operation mode: 'encrypt' or 'decrypt'."
    )
    parser.add_argument(
        "--message",
        type=str,
        required=True,
        help="The message to process."
    )
    parser.add_argument(
        "--key",
        type=int,
        required=True,
        help="The integer shift key for the Caesar cipher."
    )

    args = parser.parse_args()

    processed_message = caesar_cipher(args.message, args.key, args.mode)

    if args.mode == "encrypt":
        print(f"Encrypted message: \"{processed_message}\"")
    else:
        print(f"Decrypted message: \"{processed_message}\"")

if __name__ == "__main__":
    main()
