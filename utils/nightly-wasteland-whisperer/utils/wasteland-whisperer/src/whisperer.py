import argparse

class WastelandWhisperer:
    _SUBSTITUTION_SHIFT = 3

    _MORSE_CODE_MAP = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..',
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        '.': '.-.-.-', ',': '--..--', '?': '..--..', '/': '-..-.', '-': '-....-',
        '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...', ';': '-.-.-.',
        '=': '-...-', '+': '.-.-.', '@': '.--.-.'
    }
    _REVERSE_MORSE_CODE_MAP = {v: k for k, v in _MORSE_CODE_MAP.items()}

    def _substitute_char(self, char, shift):
        if 'A' <= char <= 'Z':
            return chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        elif 'a' <= char <= 'z':
            return chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
        elif '0' <= char <= '9':
            return chr(((ord(char) - ord('0') + shift) % 10) + ord('0'))
        return char

    def encode_substitution(self, message: str) -> str:
        encoded_chars = [self._substitute_char(char, self._SUBSTITUTION_SHIFT) for char in message]
        return ''.join(encoded_chars)

    def decode_substitution(self, encoded_message: str) -> str:
        decoded_chars = [self._substitute_char(char, -self._SUBSTITUTION_SHIFT) for char in encoded_message]
        return ''.join(decoded_chars)

    def encode_morse(self, message: str) -> str:
        words = message.upper().split(' ')
        encoded_words = []
        for word in words:
            encoded_chars = []
            for char in word:
                if char in self._MORSE_CODE_MAP:
                    encoded_chars.append(self._MORSE_CODE_MAP[char])
                # Non-mappable characters are ignored
            if encoded_chars:
                encoded_words.append(' '.join(encoded_chars))
        return ' / '.join(encoded_words)

    def decode_morse(self, encoded_message: str) -> str:
        decoded_words = []
        # Morse code words are separated by ' / '
        words_morse = encoded_message.split(' / ')
        for word_morse in words_morse:
            # Chars within a word are separated by ' '
            chars_morse = word_morse.split(' ')
            decoded_chars = []
            for char_morse in chars_morse:
                if char_morse and char_morse in self._REVERSE_MORSE_CODE_MAP:
                    decoded_chars.append(self._REVERSE_MORSE_CODE_MAP[char_morse])
                # If an unknown sequence or empty string, it's ignored
            if decoded_chars:
                decoded_words.append(''.join(decoded_chars))
        return ' '.join(decoded_words)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer: Encode/decode messages for post-apocalyptic communication."
    )
    parser.add_argument(
        "action",
        choices=["encode", "decode"],
        help="Action to perform: 'encode' or 'decode'."
    )
    parser.add_argument(
        "message",
        type=str,
        help="The message to encode or decode."
    )
    parser.add_argument(
        "--method",
        choices=["substitution", "morse"],
        default="substitution",
        help="Encoding/decoding method: 'substitution' (default) or 'morse'."
    )

    args = parser.parse_args()
    whisperer = WastelandWhisperer()

    if args.action == "encode":
        if args.method == "substitution":
            result = whisperer.encode_substitution(args.message)
        elif args.method == "morse":
            result = whisperer.encode_morse(args.message)
    elif args.action == "decode":
        if args.method == "substitution":
            result = whisperer.decode_substitution(args.message)
        elif args.method == "morse":
            result = whisperer.decode_morse(args.message)

    print(result)

if __name__ == "__main__":
    main()
