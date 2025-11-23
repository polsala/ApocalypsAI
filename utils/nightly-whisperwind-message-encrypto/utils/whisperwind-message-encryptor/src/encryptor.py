import argparse

def caesar_cipher(text: str, shift: int, mode: str = 'encrypt') -> str:
    """
    Applies a Caesar cipher to the given text.

    Args:
        text (str): The input string to encrypt or decrypt.
        shift (int): The number of positions to shift characters.
        mode (str): 'encrypt' to encrypt, 'decrypt' to decrypt.

    Returns:
        str: The processed string.
    """
    result = []
    effective_shift = shift % 26 # Ensure shift is within 0-25
    if mode == 'decrypt':
        effective_shift = -effective_shift

    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            shifted_char = chr((ord(char) - start + effective_shift) % 26 + start)
            result.append(shifted_char)
        elif 'A' <= char <= 'Z':
            start = ord('A')
            shifted_char = chr((ord(char) - start + effective_shift) % 26 + start)
            result.append(shifted_char)
        else:
            result.append(char) # Non-alphabetic characters are unchanged
    return "".join(result)

def main():
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt messages using a Caesar cipher."
    )
    parser.add_argument(
        "--text",
        type=str,
        required=True,
        help="The message text to process."
    )
    parser.add_argument(
        "--shift",
        type=int,
        required=True,
        help="The shift value for the cipher (an integer)."
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=['encrypt', 'decrypt'],
        default='encrypt',
        help="Operation mode: 'encrypt' or 'decrypt'."
    )

    args = parser.parse_args()
    processed_text = caesar_cipher(args.text, args.shift, args.mode)
    print(processed_text)

if __name__ == "__main__":
    main()
