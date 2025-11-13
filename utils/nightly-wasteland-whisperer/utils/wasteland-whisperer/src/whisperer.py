import argparse

# ApocalypsAI Morse Code Mapping
# Using standard International Morse Code for alphanumeric and common punctuation.
# Space is mapped to '|' for clarity in the encoded string.
# Unsupported characters will be mapped to '~' during encoding and '?' during decoding.
_APOCALYPSAI_MORSE_MAP = {
    'A': '._', 'B': '_...', 'C': '_._.', 'D': '_..', 'E': '.', 'F': '.._.', 'G': '__.', 'H': '....',
    'I': '..', 'J': '.___', 'K': '_._', 'L': '._..', 'M': '__', 'N': '_.', 'O': '___', 'P': '.__.',
    'Q': '__._', 'R': '._.', 'S': '...', 'T': '_', 'U': '.._', 'V': '..._', 'W': '.__', 'X': '_.._',
    'Y': '_.__', 'Z': '__..',
    '0': '_____', '1': '._ _ _ _', '2': '.._ _ _', '3': '..._ _', '4': '...._', '5': '.....',
    '6': '_....', '7': '__...', '8': '___..', '9': '____.',
    ' ': '|',  # Custom mapping for space
    '.': '._._._', ',': '__..__', '?': '..__..', '!': '_._ _ _',
    # Placeholder for unsupported characters during encoding
    'UNSUPPORTED': '~'
}

# Invert the map for decoding.
# Handle the special case of 'UNSUPPORTED' mapping to '?' during decoding.
_DECODING_MAP = {v: k for k, v in _APOCALYPSAI_MORSE_MAP.items() if k != 'UNSUPPORTED'}
_DECODING_MAP['~'] = '?' # Map the unsupported symbol back to '?'

def encode(message: str) -> str:
    """
    Encodes a plain text message into ApocalypsAI Morse.
    Unsupported characters are replaced with the '~' symbol.
    Each encoded character sequence is separated by a space.
    """
    encoded_parts = []
    for char in message.upper():
        if char in _APOCALYPSAI_MORSE_MAP:
            encoded_parts.append(_APOCALYPSAI_MORSE_MAP[char])
        else:
            encoded_parts.append(_APOCALYPSAI_MORSE_MAP['UNSUPPORTED'])
    return ' '.join(encoded_parts)

def decode(encoded_message: str) -> str:
    """
    Decodes an ApocalypsAI Morse message back to plain text.
    Each encoded character sequence is expected to be separated by a space.
    Unknown or malformed sequences are decoded as '?'.
    """
    decoded_parts = []
    
    # Split by space, then process each part. '|' will be decoded to a space.
    parts = encoded_message.split(' ')
    for part in parts:
        if part in _DECODING_MAP:
            decoded_parts.append(_DECODING_MAP[part])
        else:
            decoded_parts.append('?') # Unknown sequence
    return ''.join(decoded_parts)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer: ApocalypsAI Morse Encoder/Decoder."
    )
    parser.add_argument(
        "action",
        choices=["encode", "decode"],
        help="Action to perform: 'encode' a message or 'decode' an ApocalypsAI Morse string."
    )
    parser.add_argument(
        "message",
        help="The message to encode or the ApocalypsAI Morse string to decode."
    )

    args = parser.parse_args()

    if args.action == "encode":
        result = encode(args.message)
        print(result)
    elif args.action == "decode":
        result = decode(args.message)
        print(result)

if __name__ == "__main__":
    main()
