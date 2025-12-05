import argparse

def xor_cipher(text: str, key: str) -> str:
    """
    Encodes a string using a repeating-key XOR cipher, returning a hex string.
    """
    if not key:
        raise ValueError("Key cannot be empty.")

    text_bytes = text.encode('utf-8')
    key_bytes = key.encode('utf-8')
    result_bytes = bytearray()

    for i, byte in enumerate(text_bytes):
        result_bytes.append(byte ^ key_bytes[i % len(key_bytes)])

    return result_bytes.hex()

def xor_decipher(hex_encoded_text: str, key: str) -> str:
    """
    Decodes a hex-encoded string using a repeating-key XOR cipher.
    """
    if not key:
        raise ValueError("Key cannot be empty.")

    try:
        encoded_bytes = bytes.fromhex(hex_encoded_text)
    except ValueError:
        raise ValueError("Invalid hex string provided for decoding.")

    key_bytes = key.encode('utf-8')
    result_bytes = bytearray()

    for i, byte in enumerate(encoded_bytes):
        result_bytes.append(byte ^ key_bytes[i % len(key_bytes)])

    return result_bytes.decode('utf-8')

def main():
    parser = argparse.ArgumentParser(
        description="Whisperwind Message Encoder: Encode or decode messages using a simple XOR cipher."
    )
    parser.add_argument("mode", choices=["encode", "decode"], help="Operation mode: 'encode' or 'decode'.")
    parser.add_argument("message", help="The message to encode or the hex-encoded message to decode.")
    parser.add_argument("key", help="The secret key for encoding/decoding.")

    args = parser.parse_args()

    try:
        if args.mode == "encode":
            encoded_message = xor_cipher(args.message, args.key)
            print(f"Encoded (hex): {encoded_message}")
        elif args.mode == "decode":
            decoded_message = xor_decipher(args.message, args.key)
            print(f"Decoded: {decoded_message}")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
