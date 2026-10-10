from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Cipher Definitions ---

# Whisperwind Shift: Caesar-like cipher where shift is based on the first letter's position (A=1, B=2, etc.)
def _whisperwind_shift_cipher(text, shift, encode=True):
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            shifted_char = chr((ord(char) - start + (shift if encode else -shift)) % 26 + start)
            result.append(shifted_char)
        elif 'A' <= char <= 'Z':
            start = ord('A')
            shifted_char = chr((ord(char) - start + (shift if encode else -shift)) % 26 + start)
            result.append(shifted_char)
        else:
            result.append(char)
    return "".join(result)

def _get_whisperwind_shift_value(message):
    if not message:
        return 0
    first_char = message[0].upper()
    if 'A' <= first_char <= 'Z':
        return ord(first_char) - ord('A') + 1 # A=1, B=2, ..., Z=26
    return 0

# Void Glyph Scramble: Simple substitution cipher
VOID_GLYPH_MAP = {
    'a': '@', 'b': '#', 'c': '$', 'd': '%', 'e': '&',
    'f': '*', 'g': '+', 'h': '-', 'i': '=', 'j': '!',
    'k': '?', 'l': '/', 'm': '(', 'n': ')', 'o': '[',
    'p': ']', 'q': '{', 'r': '}', 's': '<', 't': '>',
    'u': '^', 'v': '~', 'w': '`', 'x': ';', 'y': ':',
    'z': '|',
    'A': 'Æ', 'B': 'ß', 'C': 'Ç', 'D': 'Ð', 'E': '€',
    'F': 'Ƒ', 'G': '₲', 'H': 'Ħ', 'I': 'Í', 'J': 'Ĵ',
    'K': 'Ķ', 'L': 'Ł', 'M': 'Ø', 'N': 'Ñ', 'O': 'Œ',
    'P': 'Þ', 'Q': 'Q̃', 'R': '®', 'S': '§', 'T': '†',
    'U': 'µ', 'V': '∇', 'W': '₩', 'X': '×', 'Y': '¥',
    'Z': 'Ž',
    '0': '⓪', '1': '①', '2': '②', '3': '③', '4': '④',
    '5': '⑤', '6': '⑥', '7': '⑦', '8': '⑧', '9': '⑨',
    ' ': '_',
    '.': '•', ',': '‚', '!': '¡', '?': '¿'
}

# Invert the map for decoding
VOID_GLYPH_DECODE_MAP = {v: k for k, v in VOID_GLYPH_MAP.items()}

def _void_glyph_scramble_cipher(text, encode=True):
    mapping = VOID_GLYPH_MAP if encode else VOID_GLYPH_DECODE_MAP
    result = []
    for char in text:
        result.append(mapping.get(char, char))
    return "".join(result)

# --- API Endpoints ---

@app.route('/encode', methods=['POST'])
def encode_message():
    data = request.get_json()
    if not data or 'message' not in data or 'cipher_type' not in data:
        return jsonify({"error": "Missing 'message' or 'cipher_type' in request body"}), 400

    message = data['message']
    cipher_type = data['cipher_type'].lower()

    encoded_message = ""
    if cipher_type == 'whisperwind':
        shift = _get_whisperwind_shift_value(message)
        encoded_message = _whisperwind_shift_cipher(message, shift, encode=True)
    elif cipher_type == 'void_glyph':
        encoded_message = _void_glyph_scramble_cipher(message, encode=True)
    else:
        return jsonify({"error": f"Unknown cipher type: {cipher_type}"}), 400

    return jsonify({
        "original_message": message,
        "cipher_type": cipher_type,
        "encoded_message": encoded_message
    })

@app.route('/decode', methods=['POST'])
def decode_message():
    data = request.get_json()
    if not data or 'message' not in data or 'cipher_type' not in data:
        return jsonify({"error": "Missing 'message' or 'cipher_type' in request body"}), 400

    message = data['message']
    cipher_type = data['cipher_type'].lower()

    decoded_message = ""
    if cipher_type == 'whisperwind':
        # For decoding Whisperwind, we need the original message's first char to get the shift
        # This is a limitation of a simple Caesar-like cipher without key transmission.
        # For this utility, we assume the *encoded* message's first char determines the shift for decoding.
        # In a real scenario, the shift would be part of the transmitted key or metadata.
        shift = _get_whisperwind_shift_value(message)
        decoded_message = _whisperwind_shift_cipher(message, shift, encode=False)
    elif cipher_type == 'void_glyph':
        decoded_message = _void_glyph_scramble_cipher(message, encode=False)
    else:
        return jsonify({"error": f"Unknown cipher type: {cipher_type}"}), 400

    return jsonify({
        "original_message": message,
        "cipher_type": cipher_type,
        "decoded_message": decoded_message
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
