import base64
import urllib.parse
import sys

def is_base64(s):
    """Checks if a string is likely Base64 encoded and can be decoded."""
    if not isinstance(s, str) or not s:
        return False
    # Base64 strings typically have a length that is a multiple of 4
    # and consist of specific characters. Padding '=' characters are optional
    # but if present, must be at the end.
    if len(s) % 4 != 0 and not s.endswith('='):
        return False
    try:
        # Attempt to decode. If it fails, it's not valid Base64.
        # We also check if the decoded string is printable to avoid false positives
        # for random binary data that might coincidentally be valid Base64.
        decoded_bytes = base64.b64decode(s, validate=True)
        decoded_str = decoded_bytes.decode('utf-8')
        # Check if the decoded string contains mostly printable characters
        # This helps filter out random binary data that might be valid base64 but not text
        if all(32 <= ord(c) <= 126 or c in '\n\r\t' for c in decoded_str):
            return True
    except (base64.binascii.Error, UnicodeDecodeError):
        pass
    return False

def decode_base64(s):
    """Decodes a Base64 string."""
    try:
        return base64.b64decode(s).decode('utf-8')
    except (base64.binascii.Error, UnicodeDecodeError):
        return None

def is_url_encoded(s):
    """Checks if a string is likely URL encoded."""
    if not isinstance(s, str) or not s:
        return False
    # A simple heuristic: check for '%' followed by two hex digits
    # and ensure it's not just a single '%' character.
    # This pattern is common in URL encoding.
    for i in range(len(s) - 2):
        if s[i] == '%' and s[i+1:i+3].isalnum(): # Check if it's hex-like
            return True
    return False

def decode_url_encoded(s):
    """Decodes a URL encoded string."""
    try:
        return urllib.parse.unquote(s)
    except Exception:
        return None

def is_hex(s):
    """Checks if a string is likely a hexadecimal representation of bytes."""
    if not isinstance(s, str) or not s:
        return False
    # Hex strings must have an even length and contain only hex characters.
    if len(s) % 2 != 0:
        return False
    try:
        # Attempt to convert to bytes. If it fails, it's not valid hex.
        bytes.fromhex(s)
        return True
    except ValueError:
        pass
    return False

def decode_hex(s):
    """Decodes a hexadecimal string."""
    try:
        return bytes.fromhex(s).decode('utf-8')
    except (ValueError, UnicodeDecodeError):
        return None

def decipher_data(input_string: str) -> tuple[str, str]:
    """Attempts to decipher an input string using various decoding methods.

    Returns a tuple: (decoded_string, encoding_type_detected)
    """
    if not input_string:
        return "", "none"

    # Try Base64 first, as it's common and can sometimes be mistaken for other things
    if is_base64(input_string):
        decoded = decode_base64(input_string)
        if decoded is not None:
            return decoded, "Base64"

    # Try URL encoding
    if is_url_encoded(input_string):
        decoded = decode_url_encoded(input_string)
        # Check if decoding actually changed the string, otherwise it might be a false positive
        if decoded is not None and decoded != input_string:
            return decoded, "URL"

    # Try Hexadecimal
    if is_hex(input_string):
        decoded = decode_hex(input_string)
        if decoded is not None:
            return decoded, "Hex"

    return input_string, "none"


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/decipherer.py \"<encoded_string>\"")
        sys.exit(1)

    input_str = sys.argv[1]
    decoded_str, encoding_type = decipher_data(input_str)

    if encoding_type != "none":
        print(f"Decoded ({encoding_type}): {decoded_str}")
    else:
        print(f"Original: {decoded_str}")


if __name__ == "__main__":
    main()
