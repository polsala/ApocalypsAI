import pytest
from src.app import app, _whisperwind_shift_cipher, _get_whisperwind_shift_value, _void_glyph_scramble_cipher, VOID_GLYPH_MAP, VOID_GLYPH_DECODE_MAP

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Mock rationale: app.test_client() is a standard Flask testing utility that simulates HTTP requests without running a live server, effectively mocking the network layer. The cipher functions are pure and don't require external mocks.

# --- Test Cipher Logic ---

def test_whisperwind_shift_value():
    assert _get_whisperwind_shift_value("Hello") == 8 # H is 8th letter
    assert _get_whisperwind_shift_value("apple") == 1 # A is 1st letter
    assert _get_whisperwind_shift_value("zulu") == 26 # Z is 26th letter
    assert _get_whisperwind_shift_value("123") == 0 # Non-alpha first char
    assert _get_whisperwind_shift_value("") == 0

def test_whisperwind_shift_encode_decode():
    # Test with 'H' (shift 8)
    message = "Hello, World!"
    shift = _get_whisperwind_shift_value(message) # H -> 8
    encoded = _whisperwind_shift_cipher(message, shift, encode=True)
    assert encoded == "Pmttw, Ewzlt!"
    decoded = _whisperwind_shift_cipher(encoded, shift, encode=False)
    assert decoded == message

    # Test with 'A' (shift 1)
    message = "Apple"
    shift = _get_whisperwind_shift_value(message) # A -> 1
    encoded = _whisperwind_shift_cipher(message, shift, encode=True)
    assert encoded == "Bqqmf"
    decoded = _whisperwind_shift_cipher(encoded, shift, encode=False)
    assert decoded == message

    # Test with 'Z' (shift 26, effectively 0)
    message = "Zebra"
    shift = _get_whisperwind_shift_value(message) # Z -> 26
    encoded = _whisperwind_shift_cipher(message, shift, encode=True)
    assert encoded == "Zebra"
    decoded = _whisperwind_shift_cipher(encoded, shift, encode=False)
    assert decoded == message

    # Test with mixed case and special characters
    message = "ApocalypsAI 123!"
    shift = _get_whisperwind_shift_value(message) # A -> 1
    encoded = _whisperwind_shift_cipher(message, shift, encode=True)
    assert encoded == "BqpdqbmqtbBJ 123!"
    decoded = _whisperwind_shift_cipher(encoded, shift, encode=False)
    assert decoded == message

def test_void_glyph_scramble_encode_decode():
    message = "hello world 123!"
    encoded = _void_glyph_scramble_cipher(message, encode=True)
    expected_encoded = "&_[[[_~[}#[_①②③¡"
    assert encoded == expected_encoded
    decoded = _void_glyph_scramble_cipher(encoded, encode=False)
    assert decoded == message

    message_upper = "HELLO WORLD"
    encoded_upper = _void_glyph_scramble_cipher(message_upper, encode=True)
    expected_encoded_upper = "Ħ€ŁŁŒ_₩Œ®ŁÐ"
    assert encoded_upper == expected_encoded_upper
    decoded_upper = _void_glyph_scramble_cipher(encoded_upper, encode=False)
    assert decoded_upper == message_upper.lower() # Void glyphs map uppercase to lowercase output

    # Test characters not in map remain unchanged
    message_unchanged = "@#$!%^&*()"
    encoded_unchanged = _void_glyph_scramble_cipher(message_unchanged, encode=True)
    assert encoded_unchanged == message_unchanged
    decoded_unchanged = _void_glyph_scramble_cipher(encoded_unchanged, encode=False)
    assert decoded_unchanged == message_unchanged

# --- Test API Endpoints ---

def test_encode_whisperwind(client):
    response = client.post('/encode', json={
        "message": "Secret message",
        "cipher_type": "whisperwind"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['original_message'] == "Secret message"
    assert data['cipher_type'] == "whisperwind"
    # S -> 19. "Secret message" -> "Vigxiv qiwweki"
    assert data['encoded_message'] == "Vigxiv qiwweki"

def test_decode_whisperwind(client):
    response = client.post('/decode', json={
        "message": "Vigxiv qiwweki",
        "cipher_type": "whisperwind"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['original_message'] == "Vigxiv qiwweki"
    assert data['cipher_type'] == "whisperwind"
    # V -> 22. "Vigxiv qiwweki" -> "Secret message"
    assert data['decoded_message'] == "Secret message"

def test_encode_void_glyph(client):
    response = client.post('/encode', json={
        "message": "ApocalypsAI is here!",
        "cipher_type": "void_glyph"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['original_message'] == "ApocalypsAI is here!"
    assert data['cipher_type'] == "void_glyph"
    assert data['encoded_message'] == "Æ[Œc@ŁypsÆÍ_Ís_ħ€®€¡"

def test_decode_void_glyph(client):
    response = client.post('/decode', json={
        "message": "Æ[Œc@ŁypsÆÍ_Ís_ħ€®€¡",
        "cipher_type": "void_glyph"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['original_message'] == "Æ[Œc@ŁypsÆÍ_Ís_ħ€®€¡"
    assert data['cipher_type'] == "void_glyph"
    assert data['decoded_message'] == "apocalypsai is here!"

def test_encode_missing_message(client):
    response = client.post('/encode', json={
        "cipher_type": "whisperwind"
    })
    assert response.status_code == 400
    assert "Missing 'message'" in response.get_json()['error']

def test_encode_missing_cipher_type(client):
    response = client.post('/encode', json={
        "message": "test"
    })
    assert response.status_code == 400
    assert "Missing 'cipher_type'" in response.get_json()['error']

def test_encode_unknown_cipher(client):
    response = client.post('/encode', json={
        "message": "test",
        "cipher_type": "unknown"
    })
    assert response.status_code == 400
    assert "Unknown cipher type" in response.get_json()['error']

def test_decode_missing_message(client):
    response = client.post('/decode', json={
        "cipher_type": "whisperwind"
    })
    assert response.status_code == 400
    assert "Missing 'message'" in response.get_json()['error']

def test_decode_missing_cipher_type(client):
    response = client.post('/decode', json={
        "message": "test"
    })
    assert response.status_code == 400
    assert "Missing 'cipher_type'" in response.get_json()['error']

def test_decode_unknown_cipher(client):
    response = client.post('/decode', json={
        "message": "test",
        "cipher_type": "unknown"
    })
    assert response.status_code == 400
    assert "Unknown cipher type" in response.get_json()['error']
