import base64
import codecs
import sys

def decode_base64(encoded_string: str) -> str | None:
    """Attempts to decode a Base64 string."""
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        return decoded_bytes.decode('utf-8')
    except (base64.binascii.Error, UnicodeDecodeError):
        return None

def decode_rot13(encoded_string: str) -> str:
    """Decodes a ROT13 string."""
    return codecs.decode(encoded_string, 'rot13')

def reverse_string(s: str) -> str:
    """Reverses a string."""
    return s[::-1]

def main():
    if len(sys.argv) < 2:
        print("Usage: python decoder.py <encoded_message>")
        sys.exit(1)

    message = sys.argv[1]
    print(f"Attempting to decode: '{message}'")
    print("-" * 30)

    results = []

    # Try Base64
    b64_decoded = decode_base64(message)
    if b64_decoded:
        results.append(f"Base64: {b64_decoded}")

    # Try ROT13
    rot13_decoded = decode_rot13(message)
    # Only add if it actually changed the message (i.e., wasn't already plain text or a non-ROT13 string)
    if rot13_decoded != message:
        results.append(f"ROT13: {rot13_decoded}")

    # Try Reverse
    reversed_str = reverse_string(message)
    # Only add if it actually changed the message
    if reversed_str != message:
        results.append(f"Reverse: {reversed_str}")

    if not results:
        print("No common encoding/cipher found or message is already plain.")
    else:
        for res in results:
            print(res)

if __name__ == "__main__":
    main()
