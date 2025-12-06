import base64
import urllib.parse
import codecs
import sys

def rot13_decode(s: str) -> str:
    """Decodes a string using ROT13."""
    return codecs.decode(s, 'rot13')

def try_decode(data_string: str) -> tuple[str, str] | None:
    """
    Attempts to decode a string using various common methods.
    Returns (decoded_string, method_name) on success, None otherwise.
    """
    decoders = [
        ("Base64", lambda s: base64.b64decode(s).decode('utf-8', errors='ignore')),
        ("URL-decode", lambda s: urllib.parse.unquote(s)),
        ("ROT13", rot13_decode),
    ]

    for method_name, decoder_func in decoders:
        try:
            decoded = decoder_func(data_string)
            # Heuristic: if the decoded string is significantly different
            # and for Base64, appears to be mostly printable characters, it's a likely success.
            if method_name == "Base64":
                # Check if it actually changed and is mostly printable ASCII or common whitespace
                if decoded != data_string and all(32 <= ord(c) <= 126 or c in '\n\r\t' for c in decoded):
                    return decoded, method_name
            elif decoded != data_string: # For URL-decode and ROT13, just check if it changed
                return decoded, method_name
        except Exception:
            pass # Ignore decoding errors and try next method

    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python decryptor.py <data_string>")
        sys.exit(1)

    input_string = sys.argv[1]
    result = try_decode(input_string)

    if result:
        decoded_string, method = result
        print(f"Successfully decrypted using {method}:")
        print(decoded_string)
    else:
        print("Could not decrypt using known methods. Original string:")
        print(input_string)

if __name__ == "__main__":
    main()
