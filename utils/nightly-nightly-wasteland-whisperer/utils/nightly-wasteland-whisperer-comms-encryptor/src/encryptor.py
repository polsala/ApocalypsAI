import argparse

def _calculate_shift(key: str) -> int:
    """Calculates the shift amount from a string key."""
    if not key:
        return 0
    # Sum of ASCII values modulo 26 to get a shift from 0-25
    return sum(ord(char) for char in key) % 26

def caesar_cipher(text: str, key: str, mode: str) -> str:
    """
    Applies a Caesar cipher to the given text.
    Mode can be 'encrypt' or 'decrypt'.
    """
    shift = _calculate_shift(key)
    if mode == 'decrypt':
        shift = -shift

    result = []
    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            result.append(shifted_char)
        elif 'A' <= char <= 'Z':
            start = ord('A')
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            result.append(shifted_char)
        else:
            result.append(char) # Non-alphabetic characters are unchanged
    return "".join(result)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer Comms Encryptor: Secure your messages with a simple Caesar cipher."
    )
    parser.add_argument('mode', choices=['encrypt', 'decrypt'],
                        help="Operation mode: 'encrypt' or 'decrypt'.")
    parser.add_argument('message', type=str,
                        help="The message to encrypt or decrypt.")
    parser.add_argument('key', type=str,
                        help="The secret key (string) for the cipher.")

    args = parser.parse_args()

    output = caesar_cipher(args.message, args.key, args.mode)
    print(output)

if __name__ == "__main__":
    main()
