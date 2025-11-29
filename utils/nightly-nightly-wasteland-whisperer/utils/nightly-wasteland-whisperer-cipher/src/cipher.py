import argparse

def caesar_cipher(text: str, shift: int, mode: str = 'encrypt') -> str:
    """
    Applies a Caesar cipher to the given text.

    Args:
        text (str): The input string to encrypt or decrypt.
        shift (int): The number of positions to shift each letter.
        mode (str): 'encrypt' to encrypt, 'decrypt' to decrypt.

    Returns:
        str: The processed string.
    """
    result = []
    # Normalize shift to be within 0-25 range
    shift = shift % 26

    if mode == 'decrypt':
        shift = -shift

    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            shifted_char = chr((ord(char) - start + shift + 26) % 26 + start)
            result.append(shifted_char)
        elif 'A' <= char <= 'Z':
            start = ord('A')
            shifted_char = chr((ord(char) - start + shift + 26) % 26 + start)
            result.append(shifted_char)
        else:
            result.append(char) # Non-alphabetic characters are unchanged
    return "".join(result)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer Cipher: Encrypt or decrypt messages using a Caesar cipher."
    )
    parser.add_argument(
        "mode",
        choices=["encrypt", "decrypt"],
        help="Operation mode: 'encrypt' to scramble, 'decrypt' to reveal."
    )
    parser.add_argument(
        "text",
        help="The message to process."
    )
    parser.add_argument(
        "--shift",
        type=int,
        required=True,
        help="The numerical shift value (e.g., 3 for a Caesar cipher)."
    )

    args = parser.parse_args()

    processed_text = caesar_cipher(args.text, args.shift, args.mode)
    print(processed_text)

if __name__ == "__main__":
    main()
